# flask_web/app.py

from flask import Flask, render_template, request
import os
import redis
app = Flask(__name__)

def search_text_file(goal_substring):
    results = 0
    words_file = os.path.join(os.path.dirname(__file__), "words.txt")
    with open(words_file, 'r') as f:
        for line in f.readlines():
            for word in line.split(' '):
                if goal_substring in word:
                    results += 1
    return str(results)

@app.route('/')
def index():
    return render_template('template.html', current="No Cache", endpoint="load")

@app.route('/use-cache')
def withCache():
    return render_template('template.html', current="Cache Used", endpoint="loadWithCache")

@app.route('/load', methods=["POST"])
def load():
    searching_for = request.json["search"]
    return 'Did the thing'


@app.route('/reset-redis-cache', methods=["POST"])
def flush_cache():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()
    return ""


@app.route('/loadWithCache', methods=["POST"])
def loadWithCache():
    searching_for = request.json["search"]
    expire_at = int(request.json["expireAt"])

    r = redis.Redis(host='localhost', port=6379, db=0)
    cached_result = r.get(searching_for)
    if cached_result is None:
        res = search_text_file(searching_for)
        r.set(searching_for, res)
        r.expire(searching_for, expire_at)
        return "set cache," + res
    return cached_result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')