""" This file handles unit tests for the REST APIs """

from pathlib import Path
import pytest
from app import create_app

@pytest.fixture()
def app():
    """initialize flask app for testing"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    """returns test_client for testing"""
    return app.test_client()

resources = Path(__file__).parent / "resources"

def test_hello(client):
    """this procedure tests the Test-API /hello"""
    response = client.get("/hello")
    assert response.status_code == 200

# Tests for /kmeans/manhattan

def test_kmeans_manhattan(client):
    """this procedure tests the API /kmeans/manhattan"""
    response = client.post("/kmeans/manhattan", data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_manhattan_params(client):
    """this procedure tests the API /kmeans/manhattan with parameters"""
    response = client.post("/kmeans/manhattan", query_string={"k": 10, "normMethod": 1, "r": 55, "maxCentroidsAbort": 15, "minPctElbow": 0.1, "c": 33, "minPctAutoCycle": 0.1, "maxAutoCycleAbort": 10}, data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_manhattan_failure(client):
    """this procedure tests the API /kmeans/manhattan"""
    response = client.post("/kmeans/manhattan")
    assert response.status_code == 400

# Tests for /kmeans/euclidean

def test_kmeans_euclidean(client):
    """this procedure tests the API /kmeans/euclidean"""
    response = client.post("/kmeans/euclidean", data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_euclidean_params(client):
    """this procedure tests the API /kmeans/euclidean with parameters"""
    response = client.post("/kmeans/euclidean", query_string={"k": 10, "normMethod": 1, "r": 55, "maxCentroidsAbort": 15, "minPctElbow": 0.1, "c": 33, "minPctAutoCycle": 0.1, "maxAutoCycleAbort": 10}, data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_euclidean_failure(client):
    """this procedure tests the API /kmeans/euclidean"""
    response = client.post("/kmeans/euclidean")
    assert response.status_code == 400

# Test for wrong path

def test_kmeans_wrong_path(client):
    """this procedure tests the API /kmeans/"""
    response = client.post("/kmeans/test")
    assert response.status_code == 400
