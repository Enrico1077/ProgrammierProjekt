FROM nogil/python

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create a working directory and copy application into container
WORKDIR /app
COPY . .

# Start webserver on port 80
CMD ["waitress-serve", "--port", "80", "--host", "0.0.0.0", "--call", "app:create_app"]