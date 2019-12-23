#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query/<string:query>", methods=["POST"])
def query():
    pass


if __name__ == "__main__":
    app.run(threaded=True, debug=True)
