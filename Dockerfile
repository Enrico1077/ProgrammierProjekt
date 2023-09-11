FROM ubuntu

# Install Linux dependencies
RUN apt-get update 
RUN apt-get -y install python3 python3-pip

# Create a working directory and copy application into container
WORKDIR /app
COPY ./app/ .

# Start API
ENTRYPOINT ["python3", "ServerTest.py"]