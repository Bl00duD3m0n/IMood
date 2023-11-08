from constants import *
from MySQLdb import _mysql
from flask import Flask, request

import json

app = Flask(__name__)

@app.route('/iMood/getEmojis', methods=['GET'])
def getEmojis():
    try:
        result = get_query("SELECT * FROM Emoji_types")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'error': str(e)})

@app.route('/iMood/login', methods=['POST'])
def usrLogin():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()  # Extract JSON data from the request
        login = data.get('login')
        password = data.get('password')
        result = get_query(f"SELECT * FROM Users WHERE Username = '{login}' AND PasswordHash = '{password}'")
        if result != ():
            return json.dumps({'status':'succes'})
    return json.dumps({'status': 'Invalid JSON data'}), 400

@app.route('/check', methods=['GET'])
def checkApi():
    try:
        result = get_query("SELECT * FROM Emoji_types")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'status': 'Alive'})
    
@app.route('/iMood/getUser/<usr_id>', methods=['GET'])
def getUser(usr_id):
    try:
        result = get_query(f"SELECT * FROM Users WHERE UserID = {usr_id}")
        return json.dumps(result)
    except Exception as e:
        return json.dumps({'error': str(e)})

def get_query(query: str):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    db.query(query)
    query_res = db.store_result()
    query_res = query_res.fetch_row(maxrows=0, how=1)
    for query_row in query_res:
        for column in query_row:
            try:
                query_row[column] = str(query_row[column], "utf-8")
            except TypeError:
                query_row[column] = 'null'
    db.close()
    return query_res

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

