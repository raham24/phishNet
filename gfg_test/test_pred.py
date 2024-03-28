import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import urllib.parse
import pandas as pd
import numpy as np

def prediction(clf,inp) :
    return clf.predict(inp)


if __name__ == "__main__":
    clf = joblib.load("gini.pkl")
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
        'HTTPS_token' : [np.nan],
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
        'age_of_domain' : [np.nan],
        'DNSRecord' : [np.nan],
        'web_traffic' : [np.nan],
        'Page_Rank' : [np.nan],
        'Google_Index' : [np.nan],
        'Links_pointing_to_page' : [np.nan],
        'Statistical_report' : [np.nan]
                             })
    inp = test_inp
    print(clf.predict(test_inp))