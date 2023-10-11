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
from ..K_Means import Kmeans as kmeans
from ..logging_config import setup_logging
from ..K_Means.Kmeans import Normmethod, DistanceMatrix
setup_logging()
logger = logging.getLogger(__name__)

bp = Blueprint('upload', __name__, url_prefix='/kmeans')

# This method/API is depricated and should no longer be used; for compatibility reasons it is still supported for the time being
@bp.route('/csv', methods=['POST'])
def handle_cvs_upload():
    """ this function handles an upload of a csv file """
    use_elbow = True
    try:
        if request.args.get('k'):
            param_k = int(request.args.get('k'))
            if param_k < 1:
                resp = make_response(
                    'The passed parameter k must be at least one.', 400)
                return resp
            use_elbow = False
    except ValueError:
        resp = make_response('The passed parameter k must be an integer.', 400)
        return resp

    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".csv"):
            try:
                csv_file = bytes_to_text(file)

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

            multiprocessing.freeze_support()
            if use_elbow:
                # use elbow algorithm to determine parameter k
                calculated_data = kmeans.kmeansMain(data)
            else:
                # don't use elbow and use the given parameter k instead
                calculated_data = kmeans.kmeansMain(data, param_k, 0)

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

# This method/API is depricated and should no longer be used; for compatibility reasons it is still supported for the time being
@bp.route('/json', methods=['POST'])
def handle_json_jpload():
    """ this function handles an upload of a json file """
    use_elbow = True
    try:
        if request.args.get('k'):
            param_k = int(request.args.get('k'))
            if param_k < 1:
                resp = make_response(
                    'The passed parameter k must be at least one.', 400)
                return resp
            use_elbow = False
    except ValueError:
        resp = make_response('The passed parameter k must be an integer.', 400)
        return resp

    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".json"):
            try:
                json_file = bytes_to_text(file)
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

            multiprocessing.freeze_support()
            if use_elbow:
                # use elbow algorithm to determine parameter k
                calculated_data = kmeans.kmeansMain(json_data)
            else:
                # don't use elbow and use the given parameter k instead
                calculated_data = kmeans.kmeansMain(json_data, param_k, 0)

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

@bp.route('/<distance_matrix>', methods=['POST'])
def handle_upload(distance_matrix):
    """ this function handles an upload of a file """
    api_str = "\"kmeans/<distance_matrix>\""

    # configuration parameters with its default values
    k = 0
    norm_method = Normmethod.none
    r = 5
    max_centroids_abort = 100
    min_pct_elbow = 0
    c = 0
    min_pct_auto_cycle = 0.5
    max_auto_cycle_abort = 25
    distance_matrix_int = DistanceMatrix.euclidean
    simultaneous_calculating = 1
    simultaneous_calculations = 8

    # check given distance_matrix
    if distance_matrix == "euclidean":
        distance_matrix_int = DistanceMatrix.euclidean
    elif distance_matrix == "manhattan":
        distance_matrix_int = DistanceMatrix.manhattan
    else:
        logging.info("The API %s was called without a valid distance matrix. Parameter passed: %s", api_str, distance_matrix)
        return createErrorResponse('No valid value for distance matrix was specified. Please specify euclidean or manhattan.', 400)

    # If parameter given, perform pausilibity check for k
    try:
        if request.args.get('k'):
            k = int(request.args.get('k'))
            if k < 1:
                logging.info(
                    "The API %s was called with invalid k. Parameter passed: %s", api_str, request.args.get('k'))
                return createErrorResponse('The passed parameter k must be at least one.', 400)
    except ValueError:
        logging.info("The API %s was called with invalid k. Parameter passed: %s",
                     api_str, request.args.get('k'))
        return createErrorResponse('The passed parameter k must be an integer.', 400)

    # If parameter given, perform pausilibity check for normMethod
    try:
        if request.args.get('normMethod'):
            norm_method = int(request.args.get('normMethod'))
            if norm_method < 0 or norm_method > 2:
                logging.info("The API %s was called with invalid normMethod. Parameter passed: %s",
                             api_str, request.args.get('normMethod'))
                return createErrorResponse(
                    'The passed parameter normMethod must be 0 for none, '
                    + '1 for min-max normalization, or 2 for z-normalization.', 400)
    except ValueError:
        logging.info("The API %s was called with invalid normMethod. Parameter passed: %s",
                     api_str, request.args.get('normMethod'))
        return createErrorResponse(
            'The passed parameter normMethod must be an integer.', 400)

    # If parameter given, perform pausilibity check for r
    try:
        if request.args.get('r'):
            r = int(request.args.get('r'))
            if r < 1:
                logging.info(
                    "The API %s was called with invalid r. Parameter passed: %s", api_str, request.args.get('r'))
                return createErrorResponse(
                    'The passed parameter r must be at least one.', 400)
    except ValueError:
        logging.info("The API %s was called with invalid r. Parameter passed: %s",
                     api_str, request.args.get('r'))
        return createErrorResponse('The passed parameter r must be an integer.', 400)

    # If parameter given, perform pausilibity check for maxCentroidsAbort
    try:
        if request.args.get('maxCentroidsAbort'):
            max_centroids_abort = int(request.args.get('maxCentroidsAbort'))
            if max_centroids_abort < 1:
                logging.info("The API %s was called with invalid maxCentroidsAbort. Parameter passed: %s",
                             api_str, request.args.get('maxCentroidsAbort'))
                return createErrorResponse(
                    'The passed parameter maxCentroidsAbort must be at least one.', 400)
    except ValueError:
        logging.info("The API %s was called with invalid maxCentroidsAbort. Parameter passed: %s",
                     api_str, request.args.get('maxCentroidsAbort'))
        return createErrorResponse(
            'The passed parameter maxCentroidsAbort must be an integer.', 400)

    # If parameter given, perform pausilibity check for minPctElbow
    try:
        if request.args.get('minPctElbow'):
            min_pct_elbow = float(request.args.get('minPctElbow'))
            if min_pct_elbow < 0 or min_pct_elbow > 100:
                logging.info(
                    "The API %s was called with invalid minPctElbow. Parameter passed: %s", api_str, request.args.get('minPctElbow'))
                return createErrorResponse(
                    'The passed parameter minPctElbow must be a percentage value (0 to 100).', 400)
    except ValueError:
        logging.info("The API %s was called with invalid minPctElbow. Parameter passed: %s",
                     api_str, request.args.get('minPctElbow'))
        return createErrorResponse(
            'The passed parameter minPctElbow must be a floating point number.', 400)

    # If parameter given, perform pausilibity check for c
    try:
        if request.args.get('c'):
            c = int(request.args.get('c'))
            if c < 1:
                logging.info(
                    "The API %s was called with invalid c. Parameter passed: %s", api_str, request.args.get('c'))
                return createErrorResponse(
                    'The passed parameter c must be at least one.', 400)
    except ValueError:
        logging.info(
            "The API %s was called with invalid c. Parameter passed: %s", api_str, request.args.get('c'))
        return createErrorResponse('The passed parameter c must be an integer.', 400)

    # If parameter given, perform pausilibity check for minPctAutoCycle
    try:
        if request.args.get('minPctAutoCycle'):
            min_pct_auto_cycle = float(request.args.get('minPctAutoCycle'))
            if min_pct_auto_cycle < 0 or min_pct_auto_cycle > 100:
                logging.info("The API %s was called with invalid minPctAutoCycle. Parameter passed: %s",
                             api_str, request.args.get('minPctAutoCycle'))
                return createErrorResponse(
                    'The passed parameter minPctAutoCycle must '
                    + 'be a percentage value (0 to 100).', 400)
    except ValueError:
        logging.info("The API %s was called with invalid minPctAutoCycle. Parameter passed: %s",
                     api_str, request.args.get('minPctAutoCycle'))
        return createErrorResponse(
            'The passed parameter minPctAutoCycle must be a floating point number.', 400)

    # If parameter given, perform pausilibity check for maxAutoCycleAbort
    try:
        if request.args.get('maxAutoCycleAbort'):
            max_auto_cycle_abort = int(request.args.get('maxAutoCycleAbort'))
            if max_auto_cycle_abort < 1:
                logging.info("The API %s was called with invalid maxAutoCycleAbort. Parameter passed: %s",
                             api_str, request.args.get('maxAutoCycleAbort'))
                return createErrorResponse(
                    'The passed parameter maxAutoCycleAbort must be at least one.', 400)
    except ValueError:
        logging.info("The API %s was called with invalid maxAutoCycleAbort. Parameter passed: %s",
                     api_str, request.args.get('maxAutoCycleAbort'))
        return createErrorResponse(
            'The passed parameter maxAutoCycleAbort must be an integer.', 400)
    
    # If parameter given, perform pausilibity check for parallelCalculations
    try:
        if request.args.get('parallelCalculations'):
            simultaneous_calculations = int(request.args.get('parallelCalculations'))
            if simultaneous_calculations < 1:
                logging.info("The API %s was called with invalid parallelCalculations. Parameter passed: %s",
                             api_str, request.args.get('parallelCalculations'))
                return createErrorResponse(
                    'The passed parameter parallelCalculations must be at least one.', 400)
            if simultaneous_calculations == 1:
                simultaneous_calculating = 0
            else:
                simultaneous_calculating = 1
    except ValueError:
        logging.info("The API %s was called with invalid parallelCalculations. Parameter passed: %s",
                     api_str, request.args.get('parallelCalculations'))
        return createErrorResponse(
            'The passed parameter parallelCalculations must be an integer.', 400)

    # Handle uploaded file
    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".csv"):
            # a csv file was uploaded
            csv_file = filestorage_to_bytes(file)

            if request.args.get('csvDecimalSeparator'):
                if request.args.get('csvDecimalSeparator').lower() == 'us':
                    try:
                        csv_content = pd.read_csv(csv_file, sep=None, decimal='.', thousands=',', engine='python')
                    except csv.Error as e:
                        logging.info("The API %s was called but the uploaded CSV file could not be processd. Error message: %s", api_str, e)
                        return createErrorResponse('The uploaded CSV file could not be processed; it may be corrupted.', 400)
                else:
                    # Use European format if US format is not explicitly specified
                    try:
                        csv_content = pd.read_csv(csv_file, sep=None, decimal=',', thousands='.', engine='python')
                    except csv.Error as e:
                        logging.info("The API %s was called but the uploaded CSV file could not be processd. Error message: %s", api_str, e)
                        return createErrorResponse('The uploaded CSV file could not be processed; it may be corrupted.', 400)
            else:
                # Use European format if US format is not explicitly specified
                try:
                    csv_content = pd.read_csv(csv_file, sep=None, decimal=',', thousands='.', engine='python')
                except csv.Error as e:
                    logging.info("The API %s was called but the uploaded CSV file could not be processd. Error message: %s", api_str, e)
                    return createErrorResponse('The uploaded CSV file could not be processed; it may be corrupted.', 400)
                except UnicodeDecodeError as e:
                    logging.info("The API %s was called but the uploaded CSV file could not be processd. Error message: %s", api_str, e)
                    return createErrorResponse('The uploaded CSV file could not be processed because it contains illegal characters.', 400)
            
            data = csv_content.to_dict(orient='records')

            # Closing the file without saving them to the hard disk.
            csv_file.close()
        elif file.filename.lower().endswith(".json"):
            # a json file was uploaded
            json_file = bytes_to_text(file)
            data = json.loads(json_file.read())

            # Closing the file without saving them to the hard disk.
            json_file.close()
        elif file.filename.lower().endswith(".xls") or file.filename.lower().endswith(".xlsx"):
            # an excel file was uploaded
            excel_file = filestorage_to_bytes(file)

            sheet_name = 0
            if request.args.get('sheetName'):
                # If a worksheet name was passed, use it, otherwise use the first worksheet
                sheet_name = request.args.get('sheetName')
            
            try:
                excel_content = pd.read_excel(excel_file, sheet_name)
            except ValueError as e:
                logging.info("The specified worksheet does not exist in the uploaded Excel file or there is no worksheet. Error message: %s", e)
                return createErrorResponse('The specified worksheet does not exist in the uploaded Excel file or there is no worksheet.', 400)
            except xlrd.biffh.XLRDError as e:
                logging.info("The uploaded Excel file could not be processed; it may be corrupted; Error message: %s", e)
                return createErrorResponse('The uploaded Excel file could not be processed; it may be corrupted.', 400)
            data = excel_content.to_dict(orient='records')

            # Closing the file without saving them to the hard disk.
            excel_file.close()
        else:
            # an unsupported file format was uploaded
            logging.info("An incorrect file format was uploaded. Filename: %s", file.filename)
            return createErrorResponse('An incorrect file format was uploaded. Only CSV, JSON, XLSX and XLS are supported.', 400)
    else:
        # Return error message if no file was uploaded
        logging.info("The API %s was called without a file.",api_str)
        return createErrorResponse('No file was uploaded.', 400)

    # execute k-Means
    if data:
        # executing k-means algorithm
        use_elbow = 1 if k == 0 else 0
        auto_cycle = 1 if c == 0 else 0
        multiprocessing.freeze_support()
        calculated_data = kmeans.kmeansMain(data, k, use_elbow, max_centroids_abort,
                                            min_pct_elbow, c, auto_cycle, min_pct_auto_cycle,
                                            max_auto_cycle_abort, r, distance_matrix_int,
                                            norm_method, simultaneous_calculating, simultaneous_calculations)
        logging.debug("Excuting k-Means with the following configuration:\n\tk: %s"
                      + "\n\tuse_elbow: %s\n\tmaxCentroidsAbort: %s\n\tminPctElbow: %s\n\tc: %s"
                      + "\n\tauto_cycle: %s\n\tminPctAutoCycle: %s\n\tmaxAutoCycleAbort: %s"
                      + "\n\tr: %s\n\tdistMat: %s\n\tnormMethod: %s", k, use_elbow, max_centroids_abort,
                      min_pct_elbow, c, auto_cycle, min_pct_auto_cycle,
                      max_auto_cycle_abort, r, distance_matrix,
                      norm_method)
        try:
            return jsonify(calculated_data)
        except TypeError:
            logging.error(
                "An error occured while converting calucalted data into JSON.")
            return createErrorResponse(
                'Internal server error: The calculated data could not be converted into JSON.',
                500)
    else:
        logging.error("An error occured while processing uploaded data.")
        return createErrorResponse('The uploaded file could not be processed.', 400)

def bytes_to_text(filestorage: FileStorage) -> io.TextIOWrapper:
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

def createErrorResponse(message: str, code: int) -> Response:
    """ this function creates a http error response with the given status code """
    error_response = {
        "error": {
            "code": code,
            "message": message
        }
    }
    resp = make_response(jsonify(error_response), code)
    return resp