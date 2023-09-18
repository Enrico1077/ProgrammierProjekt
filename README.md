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

Run the app in dev mode:

```
flask --app app run --debug
```

## Production

Run the app in production mode:

```
waitress-serve --port 5000 --host 0.0.0.0 --call app:create_app
```

## API

Hello-World-Message

```
http://localhost:5000/api/hello
```
