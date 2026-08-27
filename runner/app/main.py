from __future__ import annotations

import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path, PurePosixPath

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


RUNNER_MODE = os.getenv("RUNNER_MODE", "docker")
SANDBOX_IMAGE = os.getenv("SANDBOX_IMAGE", "pythoria-sandbox:local")
TIMEOUT_SECONDS = float(os.getenv("EXECUTION_TIMEOUT", "4"))
OUTPUT_LIMIT = int(os.getenv("OUTPUT_LIMIT", "32768"))
TEST_PATTERN = re.compile(r"(?P<name>(?:tests/)?[^\s:]+::test_[^\s]+)\s+(?P<status>PASSED|FAILED|ERROR|SKIPPED)")


class ExecutionRequest(BaseModel):
    mode: str
    files: dict[str, str] = Field(default_factory=dict)
    tests: dict[str, str] = Field(default_factory=dict)
    command: list[str]

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, value: str) -> str:
        if value not in {"run", "check", "terminal"}:
            raise ValueError("Unsupported execution mode")
        return value

    @field_validator("files", "tests")
    @classmethod
    def validate_files(cls, files: dict[str, str]) -> dict[str, str]:
        if len(files) > 32:
            raise ValueError("Too many files")
        for name, content in files.items():
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                raise ValueError("Invalid file path")
            if len(content.encode("utf-8")) > 100_000:
                raise ValueError("File too large")
        return files

    @field_validator("command")
    @classmethod
    def validate_command(cls, command: list[str]) -> list[str]:
        if not command:
            raise ValueError("Missing command")
        allowed = command[0] in {"python", "pytest"}
        if not allowed or len(command) > 10 or any(len(part) > 200 for part in command):
            raise ValueError("Unsupported command")
        return command


def clipped(value: str) -> str:
    encoded = value.encode("utf-8", errors="replace")
    if len(encoded) <= OUTPUT_LIMIT:
        return value
    return encoded[:OUTPUT_LIMIT].decode("utf-8", errors="ignore") + "\n… output truncated …\n"


def parse_tests(stdout: str, stderr: str) -> tuple[list[dict], int, int]:
    results: list[dict] = []
    seen: set[str] = set()
    for match in TEST_PATTERN.finditer(stdout + "\n" + stderr):
        name = match.group("name")
        if name in seen:
            continue
        seen.add(name)
        status = match.group("status").lower()
        results.append({"name": name.split("::")[-1], "status": status, "passed": status == "passed"})
    return results, sum(item["passed"] for item in results), len(results)


def archive_files(files: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        for name, content in files.items():
            data = content.encode("utf-8")
            info = tarfile.TarInfo(name=name)
            info.size = len(data)
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def execute_docker(request: ExecutionRequest) -> dict:
    try:
        import docker
        from docker.errors import DockerException, ImageNotFound
    except ImportError as exc:
        raise RuntimeError("Docker SDK is not installed") from exc

    client = docker.from_env(timeout=max(10, int(TIMEOUT_SECONDS + 3)))
    container = None
    executor: ThreadPoolExecutor | None = None
    started = time.monotonic()
    timed_out = False
    try:
        container = client.containers.create(
            SANDBOX_IMAGE,
            command=["sleep", "30"],
            network_disabled=True,
            mem_limit="128m",
            memswap_limit="128m",
            nano_cpus=500_000_000,
            pids_limit=64,
            cap_drop=["ALL"],
            security_opt=["no-new-privileges"],
            tmpfs={"/tmp": "rw,noexec,nosuid,nodev,size=8m"},
            environment={"PYTHONDONTWRITEBYTECODE": "1", "PYTHONUNBUFFERED": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
            working_dir="/workspace",
        )
        container.start()
        combined = {**request.files, **request.tests}
        if not container.put_archive("/workspace", archive_files(combined)):
            raise RuntimeError("Could not copy execution files")
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(
            container.exec_run,
            request.command,
            stdout=True,
            stderr=True,
            demux=True,
            workdir="/workspace",
            environment={"PYTHONPATH": "/workspace"},
            user="65532:65532",
        )
        try:
            exec_result = future.result(timeout=TIMEOUT_SECONDS)
            exit_code = exec_result.exit_code
            stdout_bytes, stderr_bytes = exec_result.output or (b"", b"")
        except FutureTimeout:
            timed_out = True
            exit_code = 124
            stdout_bytes, stderr_bytes = b"", b"Execution timed out\n"
            container.kill()
        stdout = clipped((stdout_bytes or b"").decode("utf-8", errors="replace"))
        stderr = clipped((stderr_bytes or b"").decode("utf-8", errors="replace"))
    except ImageNotFound as exc:
        raise HTTPException(status_code=503, detail=f"Sandbox image {SANDBOX_IMAGE} is not built") from exc
    except DockerException as exc:
        raise HTTPException(status_code=503, detail="Docker daemon is unavailable") from exc
    finally:
        if executor:
            executor.shutdown(wait=False, cancel_futures=True)
        if container:
            try:
                container.remove(force=True)
            except Exception:
                pass
        client.close()
    tests, tests_passed, tests_total = parse_tests(stdout, stderr) if request.mode == "check" else ([], 0, 0)
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "tests": tests,
        "tests_passed": tests_passed,
        "tests_total": tests_total,
    }


def execute_local(request: ExecutionRequest) -> dict:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="pythoria-") as temp:
        root = Path(temp)
        for name, content in {**request.files, **request.tests}.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        command = request.command
        if command[0] == "python":
            command = [sys.executable, *command[1:]]
        elif command[0] == "pytest":
            command = [sys.executable, "-m", "pytest", *command[1:]]
        env = {
            "PATH": os.getenv("PATH", ""),
            "PYTHONPATH": str(root),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        }
        try:
            result = subprocess.run(
                command,
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                check=False,
            )
            stdout, stderr, exit_code, timed_out = result.stdout, result.stderr, result.returncode, False
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
            stderr += "\nExecution timed out\n"
            exit_code, timed_out = 124, True
    stdout, stderr = clipped(stdout), clipped(stderr)
    tests, tests_passed, tests_total = parse_tests(stdout, stderr) if request.mode == "check" else ([], 0, 0)
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "tests": tests,
        "tests_passed": tests_passed,
        "tests_total": tests_total,
    }


app = FastAPI(title="Pythoria Runner", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "runner", "mode": RUNNER_MODE}


@app.post("/execute")
def execute(request: ExecutionRequest):
    return execute_local(request) if RUNNER_MODE == "local" else execute_docker(request)
