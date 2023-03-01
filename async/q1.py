
from quart import Quart

app = Quart(__name__)

@app.route('/')
async def hello():
    #return 'hello'
    return '<body><h1>Hello, World!</h1></body>'


if __name__ == "__main__":
    app.run()



