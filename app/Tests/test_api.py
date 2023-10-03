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

# Tests for /kmeans/csv

def test_kmeans_csv_elbow(client):
    """this procedure tests the API /kmeans/csv without parameter k (to use elbow instead)"""
    response = client.post("/kmeans/csv", data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_csv_k(client):
    """this procedure tests the API /kmeans/csv with parameter k"""
    response = client.post("/kmeans/csv", query_string={"k": 10}, data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_csv_failure_file(client):
    """this procedure tests the API /kmeans/csv with a wrong file format"""
    response = client.post("/kmeans/csv", query_string={"k": 10}, data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 400

def test_kmeans_csv_failure_k(client):
    """this procedure tests the API /kmeans/csv with a wrong k"""
    response = client.post("/kmeans/csv", query_string={"k": "5a"}, data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 400

# Tests for /kmeans/json

def test_kmeans_json_elbow(client):
    """this procedure tests the API /kmeans/json without parameter k (to use elbow instead)"""
    response = client.post("/kmeans/json", data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_json_k(client):
    """this procedure tests the API /kmeans/json with parameter k"""
    response = client.post("/kmeans/json", query_string={"k": 10}, data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_json_failure_file(client):
    """this procedure tests the API /kmeans/json with a wrong file format"""
    response = client.post("/kmeans/json", query_string={"k": 10}, data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 400

def test_kmeans_json_failure_k(client):
    """this procedure tests the API /kmeans/json with a wrong k"""
    response = client.post("/kmeans/json", query_string={"k": "5a"}, data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 400
