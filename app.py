from flask import Flask, request

app = Flask(__name__)


stores =[ {
    "name":"Mystore",
    "items":[{
        "name":"chair",
        "price":"$25"
    }]
}]

@app.get("/store")
def get_store():
    return {"stores":stores}
