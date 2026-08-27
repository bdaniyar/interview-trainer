from __future__ import annotations

from runner.app.main import ExecutionRequest, execute_local


def test_run_returns_stdout_and_exit_code():
    request = ExecutionRequest(mode="run", files={"main.py": "print('Hello')\n"}, command=["python", "main.py"])
    result = execute_local(request)
    assert result["stdout"] == "Hello\n"
    assert result["stderr"] == ""
    assert result["exit_code"] == 0


def test_syntax_error_is_reported():
    request = ExecutionRequest(mode="run", files={"main.py": "if True print('x')\n"}, command=["python", "main.py"])
    result = execute_local(request)
    assert result["exit_code"] != 0
    assert "SyntaxError" in result["stderr"]


def test_hidden_pytest_reports_failed_and_passed_tests():
    tests = {
        "tests/test_main.py": "from main import answer\n\ndef test_answer():\n    assert answer() == 42\n"
    }
    wrong = execute_local(
        ExecutionRequest(
            mode="check",
            files={"main.py": "def answer():\n    return 0\n"},
            tests=tests,
            command=["pytest", "-v", "--tb=short", "-p", "no:cacheprovider", "tests"],
        )
    )
    correct = execute_local(
        ExecutionRequest(
            mode="check",
            files={"main.py": "def answer():\n    return 42\n"},
            tests=tests,
            command=["pytest", "-v", "--tb=short", "-p", "no:cacheprovider", "tests"],
        )
    )
    assert wrong["exit_code"] != 0
    assert wrong["tests_total"] == 1 and wrong["tests_passed"] == 0
    assert correct["exit_code"] == 0
    assert correct["tests_total"] == 1 and correct["tests_passed"] == 1
