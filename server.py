from flask import Flask, request
from flask import send_file, make_response, send_from_directory
from flask import g, jsonify
import time
import sqlite3
import os

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATABASE = 'C:\Users\KL\PycharmProjects\untitled\database.db' # must be full path

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_appcontext
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_connection():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = connect_db()
    return db

def query_db(query, args=(), one=False):
    if not args:
        cur = g.db.execute(query)
    else:
        cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route('/api/getImage', methods=['POST','GET'])
def get_count():
    # return 'Hello World!'
    request_date = request.args.get('date', None)
    if not request_date:
        request_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    imgs = query_db("select id from img where date > datetime('%s') and date < datetime('%s 23:59:59'); " % (request_date, request_date) ,
                None)
    if imgs is None or len(imgs) == 0:
        return jsonify({"status": -1})
    else:
        return jsonify({"status": 0,"id":[x['id'] for x in imgs]})

@app.route('/api/getImageById', methods=['POST','GET'])
def get_img():
    id = request.args.get('id', None)
    if not id:
        return jsonify({"status": -1})
    else:
        img = query_db("select * from img where id=?", (id,), one=True)
        response = make_response(str(img['data']))
        response.headers['Content-Type'] = 'image/jpeg'
        return response

@app.route("/hello")
def hello():
    with open("D:/w.jpg", 'rb') as f:
        data = f.read(-1)
    response = make_response(data)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(BASE_PATH,'js'), path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(os.path.join(BASE_PATH,'img'), path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(os.path.join(BASE_PATH,'css'), path)

@app.route('/overview.html')
def send_index():
    return send_file(os.path.join(BASE_PATH, "overview.html"))

if __name__ == '__main__':
    app.run()