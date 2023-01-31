

from flask import Flask, flash, redirect, render_template, request, \
    session, abort, send_from_directory, send_file, jsonify
import json

from lagna import get_planet_data


app = Flask(__name__)


@app.route("/")
def hello():
    data = get_planet_data()
    return jsonify(data)



#@app.route(“/get-data”,methods=[“GET”,”POST”])
#def returnProdData():
#    f={}
#    return jsonify(f)

if __name__ == "__main__":
    app.run(debug=True)

