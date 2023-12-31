""" module to initialize a flask backend server """

import os
from flask import Flask, jsonify, make_response
from .routes import upload

# create flask app
def create_app(test_config=None):
    """ function to initialize a flask backend server """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.after_request
    def add_headers(response):
        """ Adding some global properties to all response headers """
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = 'application/json'
        response.headers['Cache-Control'] = 'no-store'
        return response

    # blueprint for handling http post requests
    app.register_blueprint(upload.bp)

    # a simple API to test the connection
    @app.route('/hello')
    def hello():
        msg = {
            "message": "Hello from the coolest backend server in the world!"
        }
        resp = make_response(jsonify(msg), 200)
        return resp

    return app
