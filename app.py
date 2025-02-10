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

@app.post("/store")
def create_store():
    req = request.get_json()
    new_store = {"name":req["name"], "items":[]}
    stores.append(new_store)
    return new_store, 201

