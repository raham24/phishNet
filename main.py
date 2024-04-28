import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from urllib.parse import urlparse
import pandas as pd
import numpy as np
import psycopg2 as pg
from psycopg2 import Error
import parse
from time import gmtime, strftime
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)  

@app.route('/predict', methods=['POST'])
def predict():
    print(request.data)  
    data = request.get_json()
    url = data.get('url')
    user = data.get('user')
    print(user,url)
    if url is None:
        return {'error': 'No url provided'}, 400
    prediction = pred(url,user)
    print(prediction)
    return {'prediction': prediction}

@app.route('/test', methods=['POST'])
def getwl():
    print(request.data)
    data = request.get_json()
    user = data.get('user')
    if user is None:
        return {'error': 'No url provided'}, 400
    return getwl(user)

@app.route('/addwl', methods=['POST'])
def addwl_route():
    print(request.data)
    data = request.get_json()
    url = data.get('url')
    user = data.get('user')
    if user is None:
        return {'error': 'No url provided'}, 400
    final = add_to_whitelist(user, url)
    return {'final' : final}

@app.route('/rmwl', methods=['POST'])
def rmwl_route():
    print(request.data)
    data = request.get_json()
    url = data.get('url')
    user = data.get('user')
    if user is None:
        return {'error': 'No url provided'}, 400
    result = rm_url(user, url)
    return {'final' : result}

@app.route('/getsafe', methods=['POST'])
def getsafe_route():
    print(request.data)
    data = request.get_json()
    user = data.get('user')
    if user is None:
        return {'error': 'No url provided'}, 400
    resultsafe = get_safe(user)
    resultphish = get_phish(user)
    return {'safe' : resultsafe, 'phish' : resultphish}

@app.route('/updatelist', methods=['POST'])
def uplist():
    print(request.data)
    data = request.get_json()
    user = data.get('user')
    if user is None:
        return {'error': 'No url provided'}, 400
    return getstatlist(user)

def pred(full_url, user):
    clf = joblib.load("rfc.pkl")
    url = get_useful_url(full_url)
    if (wlcheck(url, user)):
        return "Website Whitelisted"
    elif (check(url, user)):
        if (check_phish(url,user)):
            return "Phishing Website"
        else:
            return "Safe Website"
    else:
        df = parse.check_url(url)
        prediction = clf.predict(df)
        add_pred(url,user,prediction[0])
        if (prediction == 1):
            return "Safe Website"
        elif (prediction == 0):
            return "Unsafe Website"
        else:
            return "Phishing Website"

    
def get_useful_url(url):
    pars_url = urlparse(url)
    useful_url = pars_url.scheme + "://" + pars_url.netloc
    return useful_url


def dbconnect():
    try:
        connection = pg.connect("dbname=postgres user=postgres password=password")
        return connection
    except (Exception, Error) as error:
        print("Error connecting to the database")

def wlcheck(url, user):
    conn = dbconnect()
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(
        f"""
        SELECT EXISTS(SELECT 1 FROM public."whiteList" WHERE user_id={user} AND whitelisted_url='{url}' LIMIT 1)
        """
    )
    result = cursor.fetchone()[0]
    return result

def check(url, user):
    conn = dbconnect()
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(
        f"""
        SELECT EXISTS(SELECT 1 FROM public."phishingAttempts" WHERE user_id={user} AND phishing_url='{url}' LIMIT 1)
    """)
    reult = cursor.fetchone()[0]
    return reult

def check_if_exists(user,useful_url,cursor):
    try:
        cursor.execute(f"""
                        SELECT NOT EXISTS(SELECT 1 FROM public."whiteList" WHERE user_id={user} AND whitelisted_url='{useful_url}' LIMIT 1)
                        """)
    except (Exception,Error) as error:
        print(error)
        return False
    return cursor.fetchone()[0]

def add_to_whitelist(user, url):
    useful_url = get_useful_url(url)
    conn = dbconnect()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN;")
        if (check_if_exists(user, useful_url, cursor)):
            cursor.execute(f"""INSERT INTO "whiteList" (user_id, whitelisted_url)
                            VALUES ({user}, '{useful_url}')
                            """)
    except (Exception,Error) as error:
        print(error)
        return False
    conn.commit()
    cursor.close()
    conn.close()
    return useful_url

def extract_strings(array_of_tuples):
    return [element[0] for element in array_of_tuples if isinstance(element, tuple) and len(element) == 1][::-1]


def getwl(user):
    conn = dbconnect()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN;")
        cursor.execute(f"""SELECT whitelisted_url FROM public."whiteList" WHERE user_id={user}
                        """)
    except (Exception,Error) as error:
        print(error)
    result = cursor.fetchall()
    cursor.close()
    conn.close()  
    print(extract_strings(result))
    return jsonify({'wltest': extract_strings(result)})

def rm_url(user,url):
    useful_url = get_useful_url(url)
    conn = dbconnect()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN;")
        cursor.execute(f"""
                        DELETE FROM public."whiteList" WHERE user_id={user} AND whitelisted_url='{useful_url}'
                        """)
    except (Exception,Error) as error:
        print(error)
        return False
    cursor.execute("COMMIT;")
    cursor.close()
    conn.close()
    return True


def get_safe(user):
    conn = dbconnect()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN;")
        cursor.execute(f"""
                        SELECT * FROM public."phishingAttempts" WHERE decision_tree_prediction=1 AND user_id={user} 
                        """)
    except (Exception,Error) as error:
        print(error)
        return False
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(result)

def getstatlist(user):
    conn = dbconnect()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN;")
        cursor.execute(f"""SELECT phishing_url FROM public."phishingAttempts" WHERE user_id={user}
                        """)
    except (Exception,Error) as error:
        print(error)
    result = cursor.fetchall()
    cursor.close()
    conn.close()  
    print(extract_strings(result))
    return jsonify({'wltest': extract_strings(result)})

def get_phish(user):
    conn = dbconnect()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * FROM public."phishingAttempts" WHERE decision_tree_prediction=-1 AND user_id={user}
    """)
    reult = cursor.fetchone()[0]
    return reult


def check_phish(url, user):
    conn = dbconnect()
    cursor = conn.cursor()
    cursor.execute("BEGIN;")
    cursor.execute(
        f"""
        SELECT EXISTS(SELECT 1 FROM public."phishingAttempts" WHERE user_id={user} AND phishing_url='{url}' AND decision_tree_prediction = -1 LIMIT 1)
    """)
    reult = cursor.fetchone()[0]
    return reult

def add_pred(url,user,pred):
    conn = dbconnect()
    cursor = conn.cursor()
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    cursor.execute("BEGIN;")
    try:
        cursor.execute(
            f"""
            INSERT INTO public."phishingAttempts" ("timestamp", phishing_url, decision_tree_prediction, user_id)
            VALUES ('{strftime("%Y-%m-%d %H:%M:%S", gmtime())}', '{url}', {pred}, {user})
            """)
        conn.commit()
    except (Exception,Error) as error:
        print(error)
    cursor.close()
    conn.close()
    return True


"""
    This file will work like a makeshift api for front-end. You will import this into your code and call the pred() function.
    pred() will:
        1. connect to db
        2. check for whitelist
        3. if not in whitelist, check for exsisting instance (in db)
        4. if not in both, parse the URL for usefull info
        5. make a prediction using the decision tree using the parsed info.
        6. return 1,0,-1 depending on Phishing, Unsafe and Safe Websites

    Things needed from front-end:
        1. URL of the website
        2. (Not implemented rn, need to work on it next week) user_id of the person who is logged in
"""
if __name__ == "__main__": 

    app.run(port=5000)
