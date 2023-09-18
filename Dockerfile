FROM python:3.9

# Install pipenv
RUN pip install pipenv

# Create a working directory and copy application into container
WORKDIR /app
COPY . .

# Create virtual environment
RUN pipenv install --ignore-pipfile

# Install waitress, flask
RUN pipenv run pip install waitress
RUN pipenv run pip install flask

# Start webserver
CMD ["pipenv", "run", "start"]