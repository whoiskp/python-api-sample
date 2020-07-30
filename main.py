from flask import Flask, request
from flask_pymongo import PyMongo
from flask_redis import Redis

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://my_mongo:27017/demo"
app.config['REDIS_URL'] = 'redis://my_redis:6379/1'

mongo = PyMongo(app)
redis = Redis(app, 'REDIS')


@app.route('/')
def hello_world():
    return 'Hello, Fresher!'

@app.route('/init_db')
def ini_db():
    for i in range(10):
        mongo.db.sample.insert({'name': f'value with index {i + 1} | 👍'})
    return {"msg": "init data success"}

@app.route('/sample')
def get_sample():
    res = []
    for r in mongo.db.sample.find({}):
        res.append({
            "id": str(r['_id']),
            "name": r["name"]
        })
        print(r, flush=True)

    return {
        "msg": "success", 
        "res": res
    }

@app.route('/redis', methods=['POST'])
def set_redis():
    """
    TODO: Set key:value to redis with TTL

    @payload: json:
        - key (string): key for set
        - val (string): value for set
        - ttl ? int: 
    """
    payload = request.json

    redis.setex(
        payload['key'], 
        payload['ttl'], 
        payload['val']
    )

    print(payload, flush=True)

    return payload

@app.route('/redis/<key>')
def get_redis(key):
    val = redis.get(key)
    print(val, flush=True)
    # print(val)
    return {"key": key, "val": val.decode('utf-8')}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
