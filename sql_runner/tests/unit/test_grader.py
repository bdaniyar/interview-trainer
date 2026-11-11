from copy import deepcopy
import json

import pytest

from sql_runner.app.config import Settings
from sql_runner.app.docker_backend import QueryDeadline, SandboxUnavailable
from sql_runner.app.grader import check
from sql_runner.app.grading_content import GRADER_REVISION, TASK_ID, load_task
from sql_runner.app.lifecycle import Manager, SessionError
from sql_runner.tests.unit.test_comparator import result

QUERY = "SELECT id AS user_id,email FROM users"


class Backend:
    def __init__(self):
        self.handles = set()
        self.serial = 0
        self.max_live = 0
        self.calls = {}
        self.fail = None
        self.student = None
        self.fail_remove = False

    def create(self, *_args, **_kwargs):
        self.serial += 1
        handle = str(self.serial)
        self.handles.add(handle)
        self.max_live = max(self.max_live, len(self.handles))
        self.calls[handle] = 0
        return handle

    def install_fixture(self, *_):
        pass

    def remove(self, handle):
        if self.fail_remove:
            raise SandboxUnavailable()
        self.handles.discard(handle)

    def live_count(self):
        return len(self.handles)

    def reap(self, known):
        for handle in self.handles - known:
            self.remove(handle)

    def execute(self, handle, operation, payload):
        self.calls[handle] += 1
        if self.calls[handle] == 2:
            if self.fail:
                raise self.fail
            if self.student:
                return deepcopy(self.student)
        return result([["1", "private@example.test"]], ("int8", "text"), ["user_id", "email"])

    def close(self):
        pass


@pytest.fixture
def manager():
    backend = Backend()
    manager = Manager(Settings(), backend)
    yield manager
    backend.fail_remove = False
    manager.shutdown()


def grade(manager, query=QUERY):
    return check(manager, TASK_ID, 1, GRADER_REVISION, query)


def test_sequential_grade_preserves_live_explorer_and_uses_only_one_extra_slot(manager):
    session = manager.create()
    handle = manager.sessions[session["session_id"]].handle
    output = grade(manager)
    assert output["passed"] and output["tests_passed"] == output["tests_total"] == 4
    assert manager.backend.handles == {handle} and manager.backend.max_live == 2
    assert manager.sessions[session["session_id"]].generation == 1
    assert "private@example.test" not in json.dumps(output)


def test_full_capacity_refuses_check_without_evicting_sessions(manager):
    manager.create(); manager.create()
    before = manager.backend.handles.copy()
    with pytest.raises(SessionError) as error:
        grade(manager)
    assert error.value.status == 429 and manager.backend.handles == before


@pytest.mark.parametrize("query", ["SELECT 1; SELECT 2", "DELETE FROM users", "SELECT pg_read_file('/x')"])
def test_policy_failure_creates_no_container(manager, query):
    output = grade(manager, query)
    assert not output["passed"] and output["feedback"] == [{"code": "policy", "sqlstate": None}]
    assert manager.backend.serial == 0


def test_hidden_error_values_and_diagnostics_do_not_cross_the_boundary(manager):
    manager.backend.student = dict(error={"kind": "postgres", "sqlstate": "22P02",
        "message": "invalid input private@example.test", "detail": "hidden row", "hint": "reference SQL"})
    output = grade(manager)
    assert not output["passed"] and output["feedback"] == [{"code": "sql_error", "sqlstate": "22P02"}]
    assert "private" not in json.dumps(output) and not manager.backend.handles


def test_external_timeout_fails_and_crashed_sandbox_is_infrastructure_error(manager):
    manager.backend.fail = QueryDeadline()
    output = grade(manager)
    assert not output["passed"] and output["feedback"][0]["code"] == "timeout"
    assert not manager.backend.handles
    manager.backend.fail = SandboxUnavailable("private details")
    with pytest.raises(SessionError) as error:
        grade(manager)
    assert error.value.status == 503 and "private" not in str(error.value)
    assert not manager.backend.handles


def test_failed_cleanup_holds_capacity_and_reaper_retries(manager):
    manager.backend.fail_remove = True
    with pytest.raises(SessionError, match="cleanup"):
        grade(manager)
    assert manager.grading_handles and len(manager.backend.handles) == 1
    manager.backend.fail_remove = False
    manager.reap()
    assert not manager.grading_handles and not manager.backend.handles


def test_unknown_config_and_immutable_bundle():
    task = load_task()
    assert len(task.cases) == 4 and task.cases[-1].seed == ""
    with pytest.raises(ValueError):
        load_task("../../etc/passwd")
