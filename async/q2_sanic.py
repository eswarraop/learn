
from lagna import get_planet_data
from sanic import Sanic
from sanic_ext import render
from sanic import json
from pathlib import Path

app = Sanic(__name__)
app.extend(
config={ "templating_path_to_templates": Path(__file__).parent / "templates" }
)


@app.get("/")
@app.ext.template("index.html")
async def hello(request):
    return await render(context={})

@app.get("/stuff")
async def stuff(request):
    f=get_planet_data()
    return json(f)


#@app.route("/api")
#async def json():
#    return {"hello": "world"}
#
#@app.websocket("/ws")
#async def ws():
#    while True:
#        await websocket.send("hello")
#        await websocket.send_json({"hello": "world"})

#@app.route("/stuff",methods=["GET"])
#def stuff():
#    f=get_planet_data()
#    return jsonify(f)


if __name__ == "__main__":
    app.run(port=8192, host='0.0.0.0')

