""" module to handle incoming http post requests """

import csv
import io
import json
import logging
import multiprocessing
import pandas as pd
from flask import (Blueprint, Response, make_response, request, jsonify)
from werkzeug.datastructures import FileStorage
import xlrd
from ..k_means import k_means as kmeans
from ..logging_config import setup_logging
from ..k_means.parameter import KMeansParameter

# initialize logger with global configurations
setup_logging()
logger = logging.getLogger(__name__)

# initialize blueprint for the route '/kmeans'
bp = Blueprint('upload', __name__, url_prefix='/kmeans')

@bp.route('/<distance_matrix>', methods=['POST'])
def handle_upload(distance_matrix):
    """ this function handles an upload of a file """
    api_str = "\"kmeans/<distance_matrix>\""

    try:
        # create instance of KMeansParameter to handle given parameters and perform plausibility checks
        parameter = KMeansParameter(distance_matrix, request)
    except ValueError as e:
        logging.info("The API %s was called with invalid parameter %s; Parameter passed: \"%s\"", api_str, e.args[1], e.args[2])
        return create_error_response(e.args[0], 400)

    # Handle uploaded file
    if 'file' in request.files:
        try:
            data = file_to_json(request.files.get('file'), parameter.csv_decimal_separator, parameter.sheet_name)
        except ValueError as e:
            return create_error_response(e.args[0], 400)
    else:
        # Return error message if no file was uploaded
        logging.info("The API %s was called without a file.", api_str)
        return create_error_response('No file was uploaded.', 400)

    # execute k-Means
    if data:
        # executing k-means algorithm
        multiprocessing.freeze_support()
        calculated_data = kmeans.kmeansMain(data, parameter)
        logging.debug("Excuting k-Means with the following configuration:\n%s", parameter.get_values_str())
        try:
            return jsonify(calculated_data)
        except TypeError:
            logging.error(
                "An error occured while converting calucalted data into JSON.")
            return create_error_response(
                'Internal server error: The calculated data could not be converted into JSON.',
                500)
    else:
        logging.error("An error occured while processing uploaded data.")
        return create_error_response('The uploaded file could not be processed. Possibly the file is without content or corrupted.', 400)

def filestorage_to_text(filestorage: FileStorage) -> io.TextIOWrapper:
    """ this function converts a Flask FileStorage object into a FileObject (TextIOWrapper) """
    # Returns a bytes stream of the data of the uploaded file
    temp_file = filestorage_to_bytes(filestorage)
    # Conversion of the data into a file object readable in text mode
    temp_file = io.TextIOWrapper(temp_file, encoding='utf-8')
    return temp_file

def filestorage_to_bytes(filestorage: FileStorage) -> io.BytesIO:
    """ this function converts a Flask FileStorage object into a BytesIO object """
    # Returns a bytes stream of the data of the uploaded file
    temp_file = filestorage.stream
    # Set reading pointer to start position
    temp_file.seek(0)
    # Conversion of the stream into readable bytes
    temp_file = io.BytesIO(temp_file.read())
    return temp_file

def create_error_response(message: str, code: int) -> Response:
    """ this function creates a http error response with the given status code """
    error_response = {
        "error": {
            "code": code,
            "message": message
        }
    }
    resp = make_response(jsonify(error_response), code)
    return resp

def file_to_json(file: FileStorage, csv_decimal_separator, sheet_name):
    """ This function converts a FileStorage type object into a JSON object depending on the file type """
    filename = file.filename.lower()
    if filename.endswith(".json"):
        # JSON uploaded
        json_file = filestorage_to_text(file)
        data = json.loads(json_file.read())
        json_file.close()
        return data

    if filename.endswith(".csv"):
        # CSV uploaded
        if csv_decimal_separator == 'EU':
            decimal_separator = ','
            thousands_separator = '.'
        elif csv_decimal_separator == 'US':
            decimal_separator = '.'
            thousands_separator = ','
        else:
            raise ValueError("The given parameter csvDecimalSeparator must be \"EU\" or \"US\"", "csvDecimalSeparator", csv_decimal_separator)

        try:
            csv_file = filestorage_to_bytes(file)
            csv_content = pd.read_csv(csv_file, sep=None, decimal=decimal_separator, thousands=thousands_separator, engine='python')
        except csv.Error as e:
            logging.info("The uploaded CSV file could not be processed: %s", e)
            raise ValueError("The uploaded CSV file could not be processed. Possibly the file is without content or corrupted.") from e
        except UnicodeDecodeError as e:
            logging.info("The uploaded CSV file could not be processed: %s", e)
            raise ValueError("The uploaded CSV file could not be processed. Possibly the file is without content or corrupted.") from e

        data = csv_content.to_dict(orient='records')
        csv_file.close()
        return data

    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        # Excel uploaded
        excel_file = filestorage_to_bytes(file)

        try:
            excel_content = pd.read_excel(excel_file, sheet_name)
        except ValueError as e:
            logging.info("The uploaded Excel file could not be processed: %s", e)
            raise ValueError("The uploaded Excel file could not be processed. Possibly the file is without content or corrupted.") from e
        except xlrd.biffh.XLRDError as e:
            logging.info("The uploaded Excel file could not be processed: %s", e)
            raise ValueError("The uploaded Excel file could not be processed. Possibly the file is without content or corrupted.") from e

        data = excel_content.to_dict(orient='records')
        excel_file.close()
        return data

    # unsupported file format uploaded
    raise ValueError("An incorrect file format was uploaded; Filename: " + filename + ".")
