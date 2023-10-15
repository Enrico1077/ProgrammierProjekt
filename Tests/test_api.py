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

def test_kmeans_manhattan_params_json(client):
    """this procedure tests the API /kmeans/manhattan with parameters and json file"""
    response = client.post("/kmeans/manhattan", query_string={"k": 10, "normMethod": 1, "r": 5,
                                                              "maxCentroidsAbort": 15, "minPctElbow": 0.1,
                                                              "c": 10, "minPctAutoCycle": 0.1, "maxAutoCycleAbort": 10,
                                                              "csvDecimalSeparator": "US", "sheetName": "Tabelle1",
                                                              "parallelCalculations": 8
                                                              }, data={
        "file": (resources / "example.json").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_manhattan_params_csvus(client):
    """this procedure tests the API /kmeans/manhattan with parameters and csv file"""
    response = client.post("/kmeans/manhattan", query_string={"k": 10, "normMethod": 1, "r": 5,
                                                              "maxCentroidsAbort": 15, "minPctElbow": 0.1,
                                                              "c": 10, "minPctAutoCycle": 0.1, "maxAutoCycleAbort": 10,
                                                              "csvDecimalSeparator": "US", "sheetName": "Tabelle1",
                                                              "parallelCalculations": 8
                                                              }, data={
        "file": (resources / "example_US.csv").open("rb")
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

def test_kmeans_euclidean_params_csveu(client):
    """this procedure tests the API /kmeans/euclidean with parameters and csv file"""
    response = client.post("/kmeans/euclidean", query_string={"k": 10, "normMethod": 1, "r": 5,
                                                              "maxCentroidsAbort": 15, "minPctElbow": 0.1,
                                                              "c": 10, "minPctAutoCycle": 0.1, "maxAutoCycleAbort": 10,
                                                              "csvDecimalSeparator": "EU", "sheetName": "Tabelle1",
                                                              "parallelCalculations": 8
                                                              }, data={
        "file": (resources / "example.csv").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_euclidean_params_excel(client):
    """this procedure tests the API /kmeans/euclidean with parameters and xlsx file"""
    response = client.post("/kmeans/euclidean", query_string={"k": 10, "normMethod": 1, "r": 5,
                                                              "maxCentroidsAbort": 15, "minPctElbow": 0.1,
                                                              "c": 10, "minPctAutoCycle": 0.1, "maxAutoCycleAbort": 10,
                                                              "csvDecimalSeparator": "EU", "sheetName": "Tabelle1",
                                                              "parallelCalculations": 8
                                                              }, data={
        "file": (resources / "example.xlsx").open("rb")
    })
    assert response.status_code == 200

def test_kmeans_euclidean_params_excel(client):
    """this procedure tests the API with wrong parameters"""
    response = client.post("/kmeans/euclidean", query_string={"k": "a", "normMethod": "a", "r": "a",
                                                              "maxCentroidsAbort": "a", "minPctElbow": "a",
                                                              "c": "a", "minPctAutoCycle": "a", "maxAutoCycleAbort": "a",
                                                              "csvDecimalSeparator": 1, "sheetName": 1,
                                                              "parallelCalculations": "a"
                                                              }, data={
        "file": (resources / "example.xlsx").open("rb")
    })
    assert response.status_code == 400

def test_kmeans_euclidean_failure(client):
    """this procedure tests the API /kmeans/euclidean"""
    response = client.post("/kmeans/euclidean")
    assert response.status_code == 400

# Test for wrong path

def test_kmeans_wrong_path(client):
    """this procedure tests the API /kmeans/"""
    response = client.post("/kmeans/test")
    assert response.status_code == 400
