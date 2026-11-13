"""Sequential disposable Check, using the runner's existing admission/budgets."""
from time import monotonic
from uuid import uuid4

from .comparator import compare, complete_reference
from .docker_backend import QueryDeadline, SandboxUnavailable
from .grading_content import UnknownTask, load_task
from .lifecycle import SessionError
from .policy import PolicyError, validate

GRADE_SECONDS = 60


def check(manager, task_id, task_revision, grader_revision, query):
    try:
        task = load_task(task_id, task_revision, grader_revision)
        validate(task.reference_sql)
    except UnknownTask:
        raise SessionError(404, "unknown_task", "Unknown SQL grading configuration") from None
    except Exception:
        raise SessionError(503, "grader_configuration", "Grading configuration is unavailable") from None

    def summary(passed, feedback):
        return dict(task_id=task.id, task_revision=task.revision, grader_revision=task.grader_revision,
                    dataset_checksum=task.dataset_checksum, passed=passed == len(task.cases),
                    tests_passed=passed, tests_total=len(task.cases), feedback=feedback)

    try:
        validate(query)
    except PolicyError:
        return summary(0, [dict(code="policy", sqlstate=None)])
    passed, feedback = 0, []
    deadline = monotonic() + GRADE_SECONDS
    # The shared operation lock prevents reaper/Run/Reset races throughout Check.
    # One additional slot is required; interactive leases are never evicted.
    with manager.admission(), manager.registry:
        manager.require_capacity()
        for case in task.cases:
            handle = None
            try:
                if monotonic() >= deadline:
                    raise SessionError(503, "grader_deadline", "Grading deadline exceeded")
                handle = manager.backend.create("grade-" + uuid4().hex, 1, lifetime=60)
                manager.grading_handles.add(handle)
                if case.seed is not None:
                    manager.backend.install_fixture(handle, case.seed)
                if monotonic() >= deadline:
                    raise SessionError(503, "grader_deadline", "Grading deadline exceeded")
                expected = manager.backend.execute(handle, "run", {"sql": task.reference_sql})
                complete_reference(expected)
                if [c["name"] for c in expected["columns"]] != list(task.expected_columns):
                    raise ValueError("Reference column contract mismatch")
                try:
                    actual = manager.backend.execute(handle, "run", {"sql": query})
                except QueryDeadline:
                    actual = dict(error={"code": "query_deadline", "kind": "resource"})
                error = actual.get("error") or {}
                state = error.get("sqlstate") or ""
                if error.get("kind") == "infrastructure" or state.startswith(("08", "58")) or state in {"57P01", "57P02", "57P03"}:
                    raise SandboxUnavailable("Grading connection failed")
                code = compare(expected, actual, comparison=task.comparison, numeric_compatible=task.numeric_compatible)
                if code == "passed":
                    passed += 1
                else:
                    # A hidden value may occur even in PostgreSQL's primary error
                    # (e.g. a failing email::integer cast). Never forward it.
                    state = (actual.get("error") or {}).get("sqlstate")
                    item = dict(code=code, sqlstate=state if state and len(state) == 5 and state.isalnum() else None)
                    if item not in feedback and len(feedback) < 4:
                        feedback.append(item)
            except SessionError:
                raise
            except (SandboxUnavailable, ValueError, KeyError, TypeError):
                raise SessionError(503, "grading_unavailable", "SQL grading infrastructure failed; retry later") from None
            finally:
                if handle:
                    try:
                        manager.backend.remove(handle)
                        manager.grading_handles.discard(handle)
                    except Exception:
                        # Keep capacity reserved and let the existing reaper retry.
                        raise SessionError(503, "grading_cleanup_pending", "Grading cleanup is pending") from None
        if monotonic() > deadline:
            raise SessionError(503, "grader_deadline", "Grading deadline exceeded")
    return summary(passed, feedback or [dict(code="passed", sqlstate=None)])
