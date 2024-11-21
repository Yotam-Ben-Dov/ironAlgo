import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def main():
    # preprocess data and initialize vectors and tags
    X_train, X_test, y_train, y_test = preprocess_data()
    # create logistic regression model (should work better for the small amount of data)
    model = train_model(X_train, y_train)
    print(get_accuracy(model, X_test, y_test))
    
def preprocess_data():
    # load, preprocess and separate data to train and test
    data = pd.read_csv("headlines.csv", encoding="latin-1")
    data["magazine"] = data["magazine"].map({"haaretz": 0, "israel hayom": 1}) # map tags to 0 1
    # transform headlines to numerical vectors
    # using countvectorizer since it worked better than Tfidf
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data["headline"])
    y = data["magazine"]
    return train_test_split(X, y, test_size=0.23)


def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def get_accuracy(model, X_test, y_test):
    y_pred = model.predict(X_test)
    return accuracy_score(y_test, y_pred)
    

if __name__ =="__main__":
    main()