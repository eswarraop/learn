

from flask import Flask, flash, redirect, render_template, request, \
    session, abort, send_from_directory, send_file, jsonify
import json



app = Flask(__name__)


@app.route("/")
def hello():
    f={}
    f['cx'] = 100
    f['cy'] = 10

    return jsonify(f)

    #return "Hello Eswar\n"


#@app.route(“/get-data”,methods=[“GET”,”POST”])
#def returnProdData():
#    f={}
#    return jsonify(f)

if __name__ == "__main__":
    app.run(debug=True)

