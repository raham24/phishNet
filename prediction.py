import pandas as pd
from urllib.parse import urlparse
from tldextract import get_tld
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


clf_gini = joblib.load('decision_tree_model.pkl')

def extract_features(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path
    tld = get_tld(url, as_object=True).suffix

    features = {
        'domain_length': len(domain),
        'path_length': len(path),
        'tld': tld,
        'num_dots': domain.count('.'),
        'num_hyphens': domain.count('-'),
        'num_digits': sum(c.isdigit() for c in domain),
        'num_special_chars': sum(not c.isalnum() for c in domain),
        'num_query_params': len(parsed_url.query.split('&')),
        'num_path_segments': len(path.split('/')),
        'https': 1 if parsed_url.scheme == 'https' else 0
    }
    return features

def predict_phishing(url):
    features = extract_features(url)
    df = pd.DataFrame([features])
    return clf_gini.predict(df)[0]

if __name__ == "__main__":
    url_to_predict = input("Enter the URL to predict: ")
    prediction = predict_phishing(url_to_predict)
    if prediction == 1:
        print(f"The URL '{url_to_predict}' is predicted to be a phishing site.")
    else:
        print(f"The URL '{url_to_predict}' is predicted to be a legitimate site.")
