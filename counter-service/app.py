import time
import os
import redis
from flask_cors import CORS

from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/count')
def perform_count():
    count = get_hit_count()
    return jsonify({'counts': count})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
