import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import urllib.parse
import pandas as pd
import numpy as np
import psycopg2 as pg
from psycopg2 import Error

def pred(url, user):
    clf = joblib.load("gini.pkl")
    cursor = dbconnect()
    if (wlcheck(url, user, cursor)):
        return -1
    elif (check(url, user, cursor)):
        return check()
    else:
        parsed = parsedurl(url)
        return prediction(parsed)


def prediction(clf,inp) :
    return clf.predict(inp)

def dbconnect():
    try:
        connection = pg.connect("dbname=postgres user=postgres password=password")
        cursor = connection.cursor()
        return cursor
    except (Exception, Error) as error:
        print("Error connecting to the database")

def wlcheck(url, user, cursor):
    return 0

def check(url, user, cursor):
    return 0

def parsedurl(url):
    test_inp = pd.DataFrame({
        
        'having_IP_Address' : [np.nan], #
        'URL_Length' : [np.nan], #
        'Shortining_Service' : [np.nan],
        'having_At_Symbol' : [np.nan], #
        'double_slash_redirecting' : [np.nan], #
        'Prefix_Suffix' : [np.nan],
        'having_Sub_Domain' : [np.nan], #
        'SSLfinal_State' : [np.nan], #
        'Domain_registeration_length': [np.nan],
        'Favicon' : [np.nan],
        'port' : [np.nan],
        'HTTPS_token' : [1],
        'Request_URL' : [np.nan],
        'URL_of_Anchor' : [np.nan],
        'Links_in_tags' : [np.nan],
        'SFH' : [np.nan],
        'Submitting_to_email' : [np.nan],
        'Abnormal_URL' : [np.nan],#
        'Redirect' : [np.nan],
        'on_mouseover' : [np.nan],
        'RightClick' : [np.nan],
        'popUpWidnow' : [np.nan],
        'Iframe' : [np.nan],
        'age_of_domain' : [np.nan],#
        'DNSRecord' : [np.nan],
        'web_traffic' : [np.nan],
        'Page_Rank' : [np.nan],
        'Google_Index' : [np.nan],
        'Links_pointing_to_page' : [np.nan],
        'Statistical_report' : [np.nan]
                             })
    return test_inp

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
    pred()