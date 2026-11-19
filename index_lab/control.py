"""Trusted controller for repeatable public runs and independent Check fixtures."""
from contextlib import contextmanager
import json
from time import monotonic, sleep
from uuid import uuid4

from index_lab.policy import indexes, plan_submission, select
from index_lab.workloads import CASES, TASKS, QUERY_SQL, LOWER_SQL, truth
from index_lab.version import fingerprint
from sql_runner.app.config import PYTHON, Settings
from sql_runner.app.docker_backend import DockerBackend, SandboxUnavailable

IMAGE = "pythoria-index-sandbox:phase9c"


class IndexBackend(DockerBackend):
    def create(self, *args, **kwargs):
        handle = super().create(*args, **kwargs)
        try:
            deadline = monotonic() + 6
            while monotonic() < deadline:
                response = self.client.containers.get(handle).exec_run(
                    ["test", "-f", "/pgdata/index-ready"], user="postgres")
                if response.exit_code == 0:
                    return handle
                sleep(.04)
            raise SandboxUnavailable("Index profile initialization expired")
        except Exception:
            self.remove(handle)
            raise

    def module(self, handle, module, payload, *, user):
        def work():
            output = self.client.containers.get(handle).exec_run(
                [PYTHON, "-m", module] + ([json.dumps(payload, ensure_ascii=False)] if payload is not None else []),
                user=user, demux=True)
            data, _ = output.output
            if output.exit_code or not data or len(data) > 1024 * 1024:
                raise SandboxUnavailable("Index profile execution failed")
            return json.loads(data)
        return self._bounded(work, handle)


@contextmanager
def disposable(namespace):
    backend = IndexBackend(Settings(image=IMAGE, namespace=namespace,
                                    absolute_seconds=60, query_seconds=20))
    handle = None
    try:
        handle = backend.create(uuid4().hex[:10], 1)
        version = backend.module(handle, "index_lab.version", None, user="65532:65532")
        if version != {"profile": "pg-index-v1", "fingerprint": fingerprint()}:
            raise SandboxUnavailable("Index image differs from workload contract")
        yield backend, handle
    finally:
        try:
            if handle:
                backend.remove(handle)
            backend.reap(set())
        finally:
            backend.close()


def assess_design(details, expected, *, workload):
    """Check index intent separately from whether the natural plan chose it."""
    if len(details) != len(expected):
        return False
    for ideal in expected:
        expected_keys = [(key.field, key.expression) for key in ideal.keys]
        candidates = [index for index in details if index.table == ideal.table
                      and index.active_only == ideal.active_only
                      and [(key.field, key.expression) for key in index.keys] == expected_keys]
        if not candidates:
            return False
        if workload and candidates[0].includes:
            return False
    return True


def nodes(plan):
    yield plan
    for child in plan.get("Plans", []):
        yield from nodes(child)


def rows_equal(result, oracle):
    return (
        not result.get("truncated")
        and not result.get("has_more")
        and [column["name"] for column in result["columns"]] == oracle[0]
        and [tuple(row) for row in result["rows"]] == oracle[1]
        and [column["pg_type"] for column in result["columns"]] == {
            "email": ["int8", "text"], "arrival": ["int8", "date"],
            "created_at": ["int8", "timestamp"]
        }[oracle[0][1]]
    )


def job(task_id, source, namespace, *, grade=False):
    task = TASKS[task_id]
    design = indexes(source) if task.subject == "index" else ()
    estimated = False
    if task.subject == "plan":
        statement, actual = plan_submission(source, estimate_allowed=not grade)
        estimated = not actual
    elif not design:
        statement = select(source)
    passed = 0
    for case in range(len(CASES) if grade else 1):
        with disposable(namespace) as (backend, handle):
            payload = {"case": case, "mode": task.subject}
            if design:
                payload["design"] = source
            installed = backend.module(handle, "index_lab.install", payload, user="postgres")
            evidence = []
            ok = not design or assess_design(design, task.designs, workload=len(task.designs) > 1)
            for query in task.queries:
                result = backend.module(handle, "index_lab.read", {
                    "sql": query if design else statement, "samples": 1 if grade else 3,
                    "baseline": QUERY_SQL if task.subject == "optimize" else None,
                    "path_proof": task.subject in ("index", "optimize"),
                    "estimated": estimated,
                }, user="65532:65532")
                if result.get("error"):
                    if (result.get("sqlstate") or "").startswith(("08", "57P", "58")):
                        raise SandboxUnavailable("Index profile infrastructure failed")
                    ok = False
                elif estimated:
                    ok = False
                else:
                    ok &= rows_equal(result["result"], truth(query, case))
                    if task.subject == "index":
                        path = list(nodes(result["controlled"]))
                        ok &= any(node.get("Index Name", "").startswith("candidate_") for node in path)
                        if query != LOWER_SQL:
                            ok &= not any(node["Node Type"] in {"Sort", "Incremental Sort"} for node in path)
                    if task.subject == "optimize":
                        conditions = [node.get("Index Cond", "") for node in nodes(result["controlled"])
                                      if node.get("Index Name") == "orders_day"]
                        ok &= any(condition.count("created_at") >= 2 for condition in conditions)
                    if task.subject == "plan":
                        ok &= "Actual Rows" in result["plan"] and "Shared Hit Blocks" in result["plan"]
                evidence.append(result)
            if not grade:
                return dict(valid=bool(ok), estimated=estimated, runs=evidence,
                            definitions=installed["definitions"])
            passed += bool(ok)
    return dict(task_id=task_id, passed=passed == len(CASES), tests_passed=passed,
                tests_total=len(CASES), revision=1)
