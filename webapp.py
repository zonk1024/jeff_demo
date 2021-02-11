#!/usr/bin/env python3

import flask


app = flask.Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)
