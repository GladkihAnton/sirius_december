import pytest
from fastapi import FastAPI

from webapp.main import create_app


@pytest.fixture(scope='session')
def app() -> FastAPI:
    return create_app()
