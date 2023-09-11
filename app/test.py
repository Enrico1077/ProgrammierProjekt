import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('test', __name__, url_prefix='/test')

# a simple page that says hello
@bp.route('/hello')
def hello():
    return 'Hello, World!'