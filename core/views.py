import json
from functools import wraps
from flask import current_app
from flask import jsonify
from flask import render_template
from flask import request
from flask import Response
from flask import send_from_directory
from flask import url_for
from core import app
from core import models
from core import utils


def jsonp(func):
    """Wraps JSONified output for JSONP requests.

    From https://gist.github.com/1094140
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get("callback", False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + "(" + data + ")"
            mimetype = "application/javascript"
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


@app.errorhandler(400)
@jsonp
def bad_request(error):
    return Response(
        status=400,
        response="400 Bad Request",
        mimetype="text/plain",
    )


@app.errorhandler(404)
@jsonp
def not_found(error):
    return Response(
        status=404,
        response="404 Not Found",
        mimetype="text/plain",
    )


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html"
    )


@app.route("/v1", methods=["GET"])
def index_v1():
    return Response(
        status=400,
        response="GET /v1/normalize/<name>\r\nGET /v1/stats/<name>",
        mimetype="text/plain",
    )


@app.route("/v1/debug")
@jsonp
def debug():
    info = {
        "URL": request.url,
        "Remote Address": request.remote_addr,
        "User-Agent": request.headers["User-Agent"],
    }
    return jsonify(info)


@app.route("/v1/normalize/<name>", methods=["GET"])
@jsonp
def normalize(name):
    return Response(
        response=utils.normalize_name(name),
        mimetype="text/plain",
    )


@app.route("/v1/stats/<name>", methods=["GET"])
@jsonp
def stats(name):
    response = {}
    norm = utils.normalize_name(name)
    if request.args.get("verbose"):
        response = {
            "name_normalized": norm,
        }
    counts = models.USName.query.get_or_404(norm)
    response["given_male"] = counts.p_given_male()
    return jsonify(response)


@app.route("/v1/transposed", methods=["GET"])
@jsonp
def transposed():
    required_params = [
        "first_name",
        "last_name",
    ]
    valid = {}
    errors = []
    for i in required_params:
        param_i = request.args.get(i, None)
        if param_i:
            valid[i] = param_i
        else:
            errors.append("{0} parameter is required".format(i))
    gender = request.args.get("gender", None)
    if gender in [None, "M", "F"]:
        valid["gender"] = gender
    else:
        errors.append("gender parameter must be 'M' or 'F'")
    if request.args.get("verbose"):
        verbose = True
    else:
        verbose = False
    if errors:
        response = jsonify({
            "errors": errors
        })
        response.status_code = 400
        return response
    else:
        return jsonify(utils.p_transposed(
            valid["first_name"],
            valid["last_name"],
            valid["gender"],
            verbose
        ))

# Fallback for static content; note that this is just for local server
# development, as in the Dreamhost environment the existence of the static
# content will override Passenger entirely.
@app.route('/<path:filename>')
def static_content(filename):
    return app.send_static_file(filename)
