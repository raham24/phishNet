import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import urllib.parse
import pandas as pd

def prediction(clf,inp) :
    return clf.predict(inp)


if __name__ == "__main__":
    clf = joblib.load("gini.pkl")
    test_inp = pd.DataFrame({'ip' : []})
    inp = test_inp
    print(prediction(clf))