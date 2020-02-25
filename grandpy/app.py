#!/usr/bin/python3
#                 __                              .__       .__    .__
#  ________ _____/  |_  ________ __  _____   ____ |__| _____|  |__ |__|
#  \___   // __ \   __\/  ___/  |  \/     \_/ __ \|  |/  ___/  |  \|  |
#   /    /\  ___/|  |  \___ \|  |  /  Y Y  \  ___/|  |\___ \|   Y  \  |
#  /_____ \\___  >__| /____  >____/|__|_|  /\___  >__/____  >___|  /__|
#        \/    \/          \/            \/     \/        \/     \/
# Made on patorjk.com

import json

import nltk
from flask_cors import CORS
from flask import Flask, render_template, jsonify, request

from grandpy.apps.query.forms import QueryForm
from grandpy.apps.query.query import Query
from grandpy.apps.gmaps.gmaps import GMapsAPI
from grandpy.apps.wiki.wiki import WikiAPI

app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "*"}})
app.config.from_pyfile("settings.py")

nltk.download("punkt")


def format_answer(place, page):
    answer = (
        f"Adresse: {place.address}\nExtract: {page.extract}\nURL: {page.url}\n"
    )
    return answer


@app.route("/")
def index():
    query_form = QueryForm()
    return render_template("index.html", form=query_form)


@app.route("/query", methods=["POST"])
def query():
    if request.method == "POST":
        try:
            query = request.form["query"]
            if query:
                parser = Query(query)
                search_term = parser.parse()
                gmaps = GMapsAPI(search_term)
                place = gmaps.run()
                if not place:
                    return jsonify(query=query, answer="Je n'ai pas compris.")
                wiki = WikiAPI()
                page = wiki.run(place)
                answer = format_answer(place, page)
                return jsonify(query=query, answer=answer)
        except Exception as e:
            print(e)
            return jsonify(query=query, answer="Je n'ai pas compris")
    return jsonify(query=query, answer="Je n'ai pas compris")


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
