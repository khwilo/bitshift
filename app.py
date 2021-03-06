"""
Module to contain all the project's Flask server plumbing.
"""

from json import dumps

from flask import Flask, make_response, render_template, request

from bitshift import assets
from bitshift.database import Database
from bitshift.languages import LANGS
from bitshift.query import parse_query, QueryParseException

app = Flask(__name__, static_folder="static", static_url_path="")
app.config.from_object("bitshift.config")

app_env = app.jinja_env
app_env.line_statement_prefix = "="
app_env.globals.update(assets=assets)

database = Database()

@app.route("/")
def index():
    return render_template("index.html", autocomplete_languages=LANGS)

@app.route("/search.json")
def search():
    def reply(json):
        resp = make_response(dumps(json))
        resp.mimetype = "application/json"
        return resp

    query = request.args.get("q")
    if not query:
        return reply({"error": "No query given"})
    try:
        tree = parse_query(query)
    except QueryParseException as exc:
        return reply({"error": exc.args[0]})

    page = request.args.get("p", 1)
    try:
        page = int(page)
    except ValueError:
        return reply({"error": u"Invalid page number: %s" % page})

    highlight = request.args.get("hl", "0")
    highlight = highlight.lower() not in ["0", "false", "no"]

    count, codelets = database.search(tree, page)
    results = [clt.serialize(highlight) for clt in codelets]
    return reply({"count": count, "results": results})

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.errorhandler(404)
def error404(error):
    return render_template("error404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
