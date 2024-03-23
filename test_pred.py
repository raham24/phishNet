import joblib
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree

def prediction(clf) :
    return clf.predict()


if __name__ == "__main__":
    clf = joblib.load("gini.pkl")
    print(prediction(clf))