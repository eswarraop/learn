
from quart import Quart, render_template, websocket, jsonify
from lagna import get_planet_data

app = Quart(__name__)

@app.route("/")
async def hello():
    return await render_template("index.html")

#@app.route("/api")
#async def json():
#    return {"hello": "world"}
#
#@app.websocket("/ws")
#async def ws():
#    while True:
#        await websocket.send("hello")
#        await websocket.send_json({"hello": "world"})

@app.route("/stuff",methods=["GET"])
def stuff():
    f=get_planet_data()
    return jsonify(f)


if __name__ == "__main__":
    app.run()

