from constants import *
from MySQLdb import _mysql
from flask import Flask, request

import json
import random
import string

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

@app.route('/iMood/register', methods=['POST'])
def usrRegister():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()  # Extract JSON data from the request
        login = data.get('login')
        password = data.get('password')
        result = get_query(f"SELECT * FROM Users WHERE Username = '{login}'")
        if result != ():
            return json.dumps({'error': f"User '{login}' already exists"}), 400
        querries = []
        querries.append(f"INSERT INTO Users(Username, Email, PasswordHash, Salt) VALUES('{login}', 'null', '{password}', '{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}')")
        insert_data(querries)
        result = get_query(f"SELECT UserID FROM Users WHERE Username = '{login}'")
        return json.dumps(result)
    
    
@app.route('/iMood/setEmoji', methods=['POST'])
def usrEmojiSet():
    # Check if the request contains JSON data
    if request.is_json:
        data = request.get_json()  # Extract JSON data from the request
        login = data.get('login')
        emoji = data.get('emoji')
        try:
            emoji = int(emoji)
        except:
            return json.dumps({'error': 'Not valid emoji id'}), 500
        result = get_query(f"SELECT UserID FROM Users WHERE Username = '{login}'")
        if result == ():
            return json.dumps({'error': f"User '{login}' does not exist"}), 400
        querries = []
        querries.append(f"UPDATE Users SET Status_emoji = {emoji} WHERE Username = '{login}'")
        try:
            insert_data(querries)
        except:
            return json.dumps({'error': 'Such emoji id does not exist'}), 400
        return json.dumps({'status': 'Succes'})

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

def insert_data(queries: list):
    db = _mysql.connect(host="localhost", user=usr,
                        password=pswd, database=dbase)
    for query in queries:
        db.query(query)
    db.commit()  # commit the changes made to the database
    db.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
