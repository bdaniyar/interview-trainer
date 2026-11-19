"""Real independent PostgreSQL sessions for the stock-increment task."""
import os
from uuid import uuid4

import pytest

from transaction_lab.advanced_increment import REFERENCE, check

pytestmark = pytest.mark.skipif(os.getenv("SQL_DOCKER_TESTS") != "1",
                                reason="Opt into disposable transaction tests")


@pytest.mark.parametrize("source,ok", [
    (REFERENCE, True),
    ("UPDATE inventory SET available=2 WHERE id=1 RETURNING id,available", False),
    ("UPDATE inventory SET available=available+1 RETURNING id,available", False),
])
def test_increment_preserves_both_writes_and_every_other_row(source, ok):
    report = check(source, "tx-increment-" + uuid4().hex[:12])
    assert report["passed"] is ok and report["tests_total"] == 6
    assert report["tests_passed"] == (6 if ok else 0)
