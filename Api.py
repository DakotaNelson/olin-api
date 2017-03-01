from flask import Flask, request
from flask_restful import Resource, Api

import psycopg2
import os
import urllib.parse

app = Flask(__name__)
api = Api(app)

todos = {'todo1':'take out trash'}

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

#CHECK THE PROCFILE! I THINK WE HAVE TO RUN THIS AS WEB

def make_conn():
    global url
    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port)
    return conn

def interact_with_database(instruction, debug=False):
    """
    debug = True: returns a string that tells you what you just did.
    debug = False: returns only cursor contents.
    """
    store = None
    conn = make_conn()
    with conn.cursor() as cur:
        # try:
        cur.execute(instruction)
        store = [row for row in cur]
        # except:
            # pass
    conn.commit()
    conn.close()
    if debug:
        if store:
            return "Your instruction was " + str(instruction) + " . Cursor output (if any) is: " + str(store)
        else:
            return "Your instruction was " + str(instruction) + " . No cursor output."
    else:
        return store


class TodoSimple(Resource):
    """a get request can have a request.form e.g. 
    get('http://localhost:5000/todo1', data = {'test': 'testing'})"""
    def get(self, todo_id):
        if request.form: 
            return interact_with_database(request.form['data'])
        else:
            try:
                return {todo_id: todos[todo_id]}
            except:
                return "todo_id = " + todo_id

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

    def post(self, todo_id):
        return("XXXXXXX", request.form)
        # todos[todo_id] = request.form['data']
        # return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) #not sure this will work
    app.run(host='0.0.0.0', debug=True, port=port)