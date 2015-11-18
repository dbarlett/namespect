import json
import unicodedata
import dateparser
import ftfy
import jellyfish
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
from mailcheck import mailcheck
from nameparser import HumanName


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
        "index.html",
        ga_property_id=app.config["GA_PROPERTY_ID"],
        ga_domain_name=app.config["GA_DOMAIN_NAME"]
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


@app.route("/v1/text/fix-encoding/<string>", methods=["GET"])
@jsonp
def fix_encoding(string):
    return jsonify({
        "fixed": ftfy.fix_encoding(string)
    })


@app.route("/v1/text/fix-text/<string>", methods=["GET"])
@jsonp
def fix_text(string):
    """See https://ftfy.readthedocs.org/en/latest/#ftfy.fix_text
    """
    return jsonify({
        "fixed": ftfy.fix_text(string)
    })


@app.route("/v1/text/explain-unicode/<string>", methods=["GET"])
@jsonp
def explain_unicode(string):
    """See ftfy.explain_unicode().
    """
    response = []
    for char in string:
        if ftfy.compatibility.is_printable(char):
            display = char
        else:
            display = char.encode("unicode-escape").decode("ascii")
        response.append({
            "code": "U+{0:04X}".format(ord(char)),
            "display": display,
            "category": unicodedata.category(char),
            "name": unicodedata.name(char, "<unknown>"),
        })
    # jsonify doesn't allow toplevel lists for security
    return jsonify({"characters": response})


@app.route("/v1/text/normalize/<string>", methods=["GET"])
@jsonp
def normalize(string):
    """Normalize a string for DB lookups.
    """
    return jsonify({
        "normalized": utils.normalize_name(string)
    })


@app.route("/v1/text/fuzzy/<string>", methods=["GET"])
@jsonp
def fuzzy(string):
    return jsonify({
        "metaphone": jellyfish.metaphone(string),
        "soundex": jellyfish.soundex(string),
        "nysiis": jellyfish.nysiis(string),
        "match_rating_codex": jellyfish.match_rating_codex(string),
    })


@app.route("/v1/text/distance/<string_1>/<string_2>", methods=["GET"])
@jsonp
def distance(string_1, string_2):
    """Compute the edit distance between two strings.
    """
    return jsonify({
        "levenshtein": jellyfish.levenshtein_distance(string_1, string_2),
        "damerau-levenshtein": jellyfish.damerau_levenshtein_distance(
            string_1,
            string_2
        ),
        "jaro": jellyfish.jaro_distance(string_1, string_2),
        "jaro-winkler": jellyfish.jaro_winkler(string_1, string_2),
        "match_rating_codex": jellyfish.match_rating_comparison(
            string_1,
            string_2
        ),
        "sift3": mailcheck.sift3_distance(string_1, string_2),
    })


@app.route("/v1/datetime/parse/<datetime>", methods=["GET"])
@jsonp
def parse_datetime(datetime):
    parsed = dateparser.parse(datetime)
    if parsed:
        response = {"iso8601": parsed.isoformat()}
    else:
        response = {"iso8601": False}
    return jsonify(response)


@app.route("/v1/name/parse/<name>", methods=["GET"])
@jsonp
def parse_name(name):
    parsed = HumanName(name)
    capitalize = request.args.get("capitalize", False)
    if capitalize and capitalize == "true":
        parsed.capitalize()
    return jsonify(parsed.as_dict())


@app.route("/v1/name/stats/<name>", methods=["GET"])
@jsonp
def stats(name):
    response = {}
    norm = utils.normalize_name(name)
    verbose = request.args.get("verbose", None)
    if verbose and verbose == "true":
        response["normalized"] = norm
    counts = models.USName.query.get_or_404(norm)
    response["given_male"] = counts.p_given_male()
    return jsonify(response)


@app.route("/v1/name/transposed", methods=["GET"])
@jsonp
def transposed():
    required_params = [
        "first",
        "last",
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
            valid["first"],
            valid["last"],
            valid["gender"],
            verbose
        ))


@app.route("/v1/email/suggest/<email>", methods=["GET"])
@jsonp
def suggest(email):
    suggestion = mailcheck.suggest(email)
    if suggestion:
        suggestion["suggestion"] = True
    else:
        suggestion = {"suggestion": False}
    return jsonify(suggestion)


# Fallback for static content; note that this is just for local server
# development, as in the DreamHost environment the existence of the static
# content will override Passenger entirely.
@app.route('/<path:filename>')
def static_content(filename):
    return app.send_static_file(filename)
