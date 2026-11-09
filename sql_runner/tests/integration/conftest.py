import os
from uuid import uuid4

import pytest

from sql_runner.app.config import LABEL, Settings
from sql_runner.app.docker_backend import DockerBackend
from sql_runner.app.lifecycle import Manager


def pytest_collection_modifyitems(items):
    if os.getenv("SQL_DOCKER_TESTS") != "1":
        for item in items:
            item.add_marker(pytest.mark.skip(reason="Opt in with scripts/test_sql_runner.sh"))


@pytest.fixture
def settings():
    return Settings(namespace="test-" + uuid4().hex[:12])


@pytest.fixture
def manager(settings):
    backend = DockerBackend(settings)
    instance = Manager(settings, backend)
    instance.start()
    try:
        yield instance
    finally:
        instance.shutdown()
        # Fresh Docker client because shutdown closes its own connection pool.
        import docker
        client = docker.from_env()
        try:
            leftovers = client.containers.list(all=True, ignore_removed=True,
                                               filters={"label": f"{LABEL}={settings.namespace}"})
            for container in leftovers:
                container.remove(force=True, v=True)
            assert leftovers == [], "Test leaked a SQL sandbox"
        finally:
            client.close()


@pytest.fixture
def session(manager):
    return manager.create()
