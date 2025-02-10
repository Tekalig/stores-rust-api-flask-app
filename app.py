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

@app.post("/store/<string:name>/item")
def add_item(name):
    req = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name":req["name"], "price":req["price"]}
            store["items"].append(new_item)
            return new_item,201
    return {"message": "Store isn't Found!"}, 404

@app.get("/store/<string:name>")
def get_specific_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store isn't Found!"}, 404

