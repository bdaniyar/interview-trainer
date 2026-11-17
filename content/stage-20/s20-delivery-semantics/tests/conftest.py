"""Keep hidden-case source and captured values out of ordinary Check diagnostics."""
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        report.longrepr = f"{item.name}: Контракт проверки не выполнен; сверьтесь с условиями урока и используйте Run для отладки своего кода."
        report.sections.clear()
