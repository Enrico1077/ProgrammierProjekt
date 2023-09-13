# ProgrammierProjekt

Backend fürs Programmier-Projekt

## Installation

To install the project's dependencies run the following command:

```
pipenv install
```

To add a new dependency to the project:

```
pipenv install <package>
```

or for dev-dependencies:

```
pipenv install --dev <package>
```

To remove a dependency from the project:

```
pipenv remove <package>
```

## Development

Run the app in dev mode:

```
flask --app app run --debug
```

## Production

Run the app in production mode:

```
pipenv run start
```

## API

Hello-World-Message

```
http://localhost/api/hello
```
