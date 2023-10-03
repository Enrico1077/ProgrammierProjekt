# ProgrammierProjekt

Backend fürs Programmier-Projekt

Development URL: https://development-ujgmkp4tpq-ez.a.run.app

Production URL: https://programmierprojekt-ujgmkp4tpq-ez.a.run.app

## Installation

To install the project's dependencies run the following command:

```
pip install -r requirements.txt
```

To add or remove dependencies to the project, edit the file "requirements.txt".

## Development

To lint all python files:

```
pylint app/*/*.py
```

Run the app in dev mode:

```
flask --app app run --debug
```

Run unit tests locally:

```
pytest app/Tests/
```

## Production

Run the app in production mode:

```
waitress-serve --port 5000 --host 0.0.0.0 --call app:create_app
```

## API

**Test API (HTTP GET):**

```
/hello
```

**Upload a CSV file (HTTP POST):**
The body must have a field called "file" which contains a CSV file as value. The parameter k can be passed optionally. If it is not passed, Elbow is used to determine the optimal k.

```
/kmeans/csv?k=10
```

**Upload a JSON file (HTTP POST):**
The body must have a field called "file" which contains a JSON file as value. The parameter k can be passed optionally. If it is not passed, Elbow is used to determine the optimal k.

```
/kmeans/json?k=10
```
