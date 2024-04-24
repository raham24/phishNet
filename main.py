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

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    print(request.data)  # Log the raw request data
    data = request.get_json()
    url = data.get('url')
    if url is None:
        return {'error': 'No url provided'}, 400
    prediction = predtest(url)
    return {'prediction': prediction}


def pred(full_url, user):
    clf = joblib.load("rfc.pkl")
    conn = dbconnect()
    cursor = conn.cursor()
    url = get_useful_url(full_url)
    if (wlcheck(url, user, cursor)):
        return "Website Whitelisted"
    elif (check(url, user, cursor)):
        if (check_phish(url,user,cursor)):
            return "Phishing Website"
        else:
            return "Safe Website"
    else:
        df = parse.check_url(url)
        prediction = clf.predict(df)
        if (prediction == 1):
            return "Safe Website"
        elif (prediction == 0):
            return "Unsafe Website"
        else:
            return "Phishing Website"

def predtest(url):
    clf = joblib.load("rfc.pkl")
    df = parse.check_url(url)
    prediction = clf.predict(df)
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

def wlcheck(url, user, cursor):
    
    cursor.execute("BEGIN;")
    cursor.execute(
        f"""
        SELECT EXISTS(SELECT 1 FROM public."whiteList" WHERE user_id={user} AND whitelisted_url='{url}' LIMIT 1)
        """
    )
    result = cursor.fetchone()[0]
    return result

def check(url, user, cursor):
    cursor.execute("BEGIN;")
    cursor.execute(
        f"""
        SELECT EXISTS(SELECT 1 FROM public."whiteList" WHERE user_id={user} AND whitelisted_url='{url}' LIMIT 1)
        """
    )
    return 0

def check_phish(url, user, cursor):
    return 0


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
if __name__ == "__main__": #purely for testing purposes, will not use in the final iteration
    app.run(port=5000)
    """
    c = dbconnect()
    url = "https://www.google.com"
    print(urlparse(url).netloc)
    print(wlcheck(url,1,c))
    df = parse.check_url(url)
    clf = joblib.load("rfc.pkl")
    print(clf.predict(df))
    print(get_useful_url("https://mail.google.com/mail/u/0/#inboxhttps://mail.google.com/mail/u/0/#inbox"))
    connector = dbconnect()
    insert_attempts(connector)
"""