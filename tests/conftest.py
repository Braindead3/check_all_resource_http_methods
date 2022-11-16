import pytest
import httpx


@pytest.fixture()
def client():
    return httpx.AsyncClient()
