"""Privileged control plane: no client-selectable image, command, mount or DSN."""
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
import json
import logging
from threading import Lock
from time import monotonic, sleep

import docker
from docker.errors import NotFound

from .config import LABEL, PYTHON, RESULT_BYTES, Settings
from .schemas import Result

log = logging.getLogger(__name__)


class SandboxUnavailable(RuntimeError):
    pass


class QueryDeadline(SandboxUnavailable):
    pass


class DockerBackend:
    def __init__(self, settings: Settings, client=None):
        self.settings = settings
        self.client = client or docker.from_env(timeout=5)
        self.client.ping()
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="sql-exec")
        self.pending = None
        self.pending_lock = Lock()

    def containers(self):
        return self.client.containers.list(all=True, ignore_removed=True,
                                           filters={"label": f"{LABEL}={self.settings.namespace}"})

    def live_count(self):
        return len(self.containers())

    def reap(self, known):
        for container in self.containers():
            if container.id not in known:
                self.remove(container.id)

    def create(self, session_id, generation):
        container = None
        deadline = monotonic() + self.settings.provision_seconds
        try:
            container = self.client.containers.create(
                self.settings.image,
                name=f"sql-{self.settings.namespace}-{session_id}-{generation}",
                labels={LABEL: self.settings.namespace, f"{LABEL}.session": session_id,
                        f"{LABEL}.generation": str(generation)},
                environment={"SQL_ABSOLUTE_SECONDS": str(self.settings.absolute_seconds)},
                network_disabled=True, network_mode="none", read_only=True,
                mem_limit="512m", memswap_limit="512m", nano_cpus=1_000_000_000,
                pids_limit=128, cap_drop=["ALL"], security_opt=["no-new-privileges:true"],
                auto_remove=True, user="postgres",
                tmpfs={"/pgdata": "rw,noexec,nosuid,nodev,size=256m,uid=999,gid=999,mode=0700",
                       "/var/run/postgresql": "rw,noexec,nosuid,nodev,size=1m,uid=999,gid=999,mode=0755",
                       "/tmp": "rw,noexec,nosuid,nodev,size=8m,mode=1777",
                       # Official image declares this VOLUME; shadow it with a
                       # bounded tmpfs so Docker creates no anonymous data volume.
                       "/var/lib/postgresql/data": "rw,noexec,nosuid,nodev,size=1m,uid=999,gid=999"},
                log_config=docker.types.LogConfig(type="json-file", config={"max-size": "1m", "max-file": "1"}),
            )
            container.start()
            while monotonic() < deadline:
                check = container.exec_run(["test", "-f", "/pgdata/ready"], user="postgres")
                if check.exit_code == 0:
                    return container.id
                container.reload()
                if container.status != "running":
                    break
                sleep(0.1)
            raise SandboxUnavailable("PostgreSQL provisioning failed or expired")
        except Exception as exc:
            if container:
                try:
                    self.remove(container.id)
                except Exception:
                    log.warning("Sandbox provisioning cleanup deferred to reaper")
            raise SandboxUnavailable("Unable to provision SQL sandbox") from exc

    def remove(self, handle):
        try:
            # Handles originate only from create/list, never from HTTP payloads.
            self.client.containers.get(handle).remove(force=True, v=True)
        except NotFound:
            pass

    def execute(self, handle, operation, payload):
        def work():
            container = self.client.containers.get(handle)
            # exec is an argv array; neither a shell nor psql parses SQL here.
            response = container.exec_run(
                [PYTHON, "-m", "sql_runner.app.executor", operation,
                 json.dumps(payload, ensure_ascii=False, separators=(",", ":"))],
                user="65532:65532", demux=True,
            )
            stdout, _stderr = response.output
            if response.exit_code != 0 or not stdout or len(stdout) > RESULT_BYTES:
                raise SandboxUnavailable("SQL executor exited or exceeded its wire budget")
            result = json.loads(stdout)
            if operation != "catalog":
                result = Result.model_validate(result).model_dump(exclude_none=False)
            return result

        with self.pending_lock:
            # A timed-out Docker RPC must not create an unbounded executor queue.
            if self.pending is not None and not self.pending.done():
                raise SandboxUnavailable("Previous Docker operation is still terminating")
            self.pending = self.pool.submit(work)
            future = self.pending
        try:
            return future.result(timeout=self.settings.query_seconds)
        except FutureTimeout:
            # Kill the actual process boundary, not just the Python Future.
            try:
                self.remove(handle)
            except Exception:
                log.warning("Query deadline cleanup deferred to reaper")
            raise QueryDeadline("External SQL query deadline exceeded") from None
        except Exception as exc:
            raise SandboxUnavailable("SQL sandbox unavailable") from exc

    def close(self):
        self.pool.shutdown(wait=False, cancel_futures=True)
        self.client.close()
