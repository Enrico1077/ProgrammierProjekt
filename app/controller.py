""" module to handle incoming http requests """

from flask import (
    Blueprint
)

bp = Blueprint('controller', __name__, url_prefix='/api')

@bp.route('/hello')
def hello():
    """ a simple page that says hello """
    return 'Hello, World!'
