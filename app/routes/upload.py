""" module to handle incoming http post requests """

from flask import (Blueprint, make_response, request)

bp = Blueprint('upload', __name__, url_prefix='/kmeans')

@bp.route('/csv/<parameter_k>', methods = ['POST'])
def handle_cvs_upload(parameter_k):
    """ this function handles an upload of a csv file """
    try:
        int(parameter_k)
    except ValueError:
        resp = make_response('The passed parameter k was not an integer.', 400)
        return resp

    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".csv"):
            # To-Do: Hier die weitere Verarbeitung der hochgeladenen Datei hinzufügen
            return "OK"
    # Return error message if no file was uploaded or it was not the correct file format
    resp = make_response('No CSV file was uploaded.', 400)
    return resp

@bp.route('/json/<parameter_k>', methods = ['POST'])
def handle_json_jpload(parameter_k):
    """ this function handles an upload of a json file """
    try:
        int(parameter_k)
    except ValueError:
        resp = make_response('The passed parameter k was not an integer.', 400)
        return resp

    if 'file' in request.files:
        file = request.files.get('file')
        if file.filename.lower().endswith(".json"):
            # To-Do: Hier die weitere Verarbeitung der hochgeladenen Datei hinzufügen
            return "OK"
    # Return error message if no file was uploaded or it was not the correct file format
    resp = make_response('No JSON file was uploaded.', 400)
    return resp
