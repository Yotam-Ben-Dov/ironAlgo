from numpy import vectorize
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords

def get_model(test_size):
    X, y, vectorizer = preprocess_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    model = train_model(X_train, y_train)
    acc = get_accuracy(model, X_test, y_test)
    print(f"generated model has {acc} accuracy")
    return model, vectorizer

def preprocess_data():
    # load, preprocess and separate data to train and test
    data = pd.read_csv("headlines.csv", encoding="utf-8")
    data["magazine"] = data["magazine"].map({"haaretz": 0, "israel hayom": 1}) # map tags to 0 1
    # transform headlines to numerical vectors
    # using countvectorizer since it worked better than Tfidf
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data["headline"])
    y = data["magazine"]
    
    return X, y, vectorizer

def train_model(X_train, y_train): # func to train model
    model = LogisticRegression(solver="liblinear") # liblinear solver is better for smaller data sets
    model.fit(X_train, y_train)
    return model

def get_accuracy(model, X_test, y_test): # gets acc
    y_pred = model.predict(X_test)
    return accuracy_score(y_test, y_pred)
    
def remove_stopwords(data): # removes stopwords from the headlines (found it to reduce acc, so deprecated)
    sw = stopwords.words("english")
    for i, s in enumerate(data["headline"]):
        wl = s.split()
        clean_h = ' '.join([word for word in wl if word not in sw])
        data.loc[i, "headline"] = clean_h # replaces old sentences with clean ones
        
def tests(): # test acc settings
    max_acc = 0
    min_acc = 1
    avg_acc = 1
    size = 0.18 # best result after tests
    print(a)
    for i in range(500):
        # preprocess data and initialize vectors and tags
        X_train, X_test, y_train, y_test = preprocess_data(size)
        # create logistic regression model (should work better for the small amount of data)
        model = train_model(X_train, y_train)
        acc = get_accuracy(model, X_test, y_test)
        max_acc = acc if max_acc < acc else max_acc
        min_acc = acc if min_acc > acc else min_acc
        avg_acc = avg_acc + acc
    avg_acc /= 500
    return max_acc, min_acc, avg_acc