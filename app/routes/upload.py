""" module to handle incoming http post requests """

import csv
import io
import json
from flask import (Blueprint, make_response, request, jsonify)
from werkzeug.datastructures import FileStorage
from ..K_Means import Kmeans as kmeans

bp = Blueprint('upload', __name__, url_prefix='/kmeans')

@bp.route('/csv/<parameter_k>', methods = ['POST'])
def handle_cvs_upload(parameter_k):
    """ this function handles an upload of a csv file """
    try:
        param_k = int(parameter_k)
        if param_k < 1:
            resp = make_response('The passed parameter k must be at least one.', 400)
            return resp
    except ValueError:
        resp = make_response('The passed parameter k must be an integer.', 400)
        return resp

    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".csv"):
            try:
                csv_file = filestorage_to_fileobject(file)

                # creating a csv reader object
                csvreader = csv.DictReader(csv_file)
                # converting the data into an array of JSON objects (one JSON object per line)
                data = list(csvreader)

                # Closing the file without saving them to the hard disk.
                csv_file.close()
            # pylint: disable=bare-except
            except:
                resp = make_response('An unexpected error occurred.', 500)
                return resp
            finally:
                # Closing the file without saving them to the hard disk.
                csv_file.close()

            calculated_data = kmeans.kmeansMain(data, param_k)

            try:
                return jsonify(calculated_data)
            except TypeError:
                resp = make_response(
                    'Internal server error: The calculated data could not be converted into JSON.',
                    500)
                return resp
    # Return error message if no file was uploaded or it was not the correct file format
    resp = make_response('No CSV file was uploaded.', 400)
    return resp

@bp.route('/json/<parameter_k>', methods = ['POST'])
def handle_json_jpload(parameter_k):
    """ this function handles an upload of a json file """
    try:
        param_k = int(parameter_k)
        if param_k < 1:
            resp = make_response('The passed parameter k must be at least one.', 400)
            return resp
    except ValueError:
        resp = make_response('The passed parameter k must be an integer.', 400)
        return resp

    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".json"):
            try:
                json_file = filestorage_to_fileobject(file)
                json_data = json.loads(json_file.read())
                # Closing the file without saving them to the hard disk.
                json_file.close()
            # pylint: disable=bare-except
            except:
                resp = make_response('An unexpected error occurred.', 500)
                return resp
            finally:
                # Closing the file without saving them to the hard disk.
                json_file.close()

            calculated_data = kmeans.kmeansMain(json_data, param_k)

            try:
                return jsonify(calculated_data)
            except TypeError:
                resp = make_response(
                    'Internal server error: The calculated data could not be converted into JSON.',
                    500)
                return resp
    # Return error message if no file was uploaded or it was not the correct file format
    resp = make_response('No JSON file was uploaded.', 400)
    return resp

def filestorage_to_fileobject(filestorage: FileStorage) -> io.TextIOWrapper:
    """ this function converts a Flask FileStorage object into a FileObject """
    # Returns a bytes stream of the data of the uploaded file
    temp_file = filestorage.stream
    # Set reading pointer to start position
    temp_file.seek(0)
    # Conversion of the stream into readable bytes
    temp_file = io.BytesIO(temp_file.read())
    # Conversion of the data into a file object readable in text mode
    temp_file = io.TextIOWrapper(temp_file, encoding='utf-8')
    return temp_file
