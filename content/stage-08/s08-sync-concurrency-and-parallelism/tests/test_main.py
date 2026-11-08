"""Accept the published v1 submission contract without deleting saved files.

New starters expose compare_waits and MUST pass the v2 tests. Only old files
which lack that name take the legacy path; there is no fallback after failure.
"""
import asyncio
import threading
import pytest
import main

IS_V2 = hasattr(main, "compare_waits")

@pytest.mark.skipif(not IS_V2, reason="saved v1 submission")
@pytest.mark.parametrize("values, expected", [([2, 3], (5, 3)), ([], (0, 0)), ([0], (0, 0)), ([0, 4, 4], (8, 4)), ([9, 1], (10, 9))])
def test_model(values, expected):
    original = values.copy()
    assert main.compare_waits(values) == expected
    assert values == original

@pytest.mark.skipif(not IS_V2, reason="saved v1 submission")
def test_negative():
    with pytest.raises(ValueError):
        main.compare_waits([2, -1])

@pytest.mark.skipif(IS_V2, reason="current v2 submission")
def test_saved_v1_contract():
    owner = threading.get_ident()
    def work(value):
        return value * 2, threading.get_ident() != owner
    result = asyncio.run(main.run_blocking_calls(work, [3, 1, 2]))
    assert [item[0] for item in result] == [6, 2, 4]
    assert all(item[1] for item in result)
    assert asyncio.run(main.run_blocking_calls(work, [])) == []
