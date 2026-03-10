import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(scope="session")
def initial_activities_snapshot():
    return copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(initial_activities_snapshot):
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(initial_activities_snapshot))
    yield


@pytest.fixture
def client():
    return TestClient(app_module.app)