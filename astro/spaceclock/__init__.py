

from flask import Flask, flash, redirect, render_template, request, \
    session, abort, send_from_directory, send_file, jsonify
import json

from .lagna import get_planet_data


app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/stuff",methods=["GET"])
def stuff():
    f=get_planet_data()
    return jsonify(f)

if __name__ == "__main__":
    app.run(debug=True)

