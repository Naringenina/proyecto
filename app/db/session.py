import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db import get_session as app_get_session  # <- OJO: la función real a override

@pytest.fixture
def engine():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def session(engine):
    with Session(engine) as s:
        yield s

@pytest.fixture
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[app_get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
