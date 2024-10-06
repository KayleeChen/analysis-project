import pandas as pd
import numpy as np
import csv
from snownlp import SnowNLP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Function to read sentiment data from a CSV file
def getSentiment_data():
    sentiment_data = []
    with open('./target.csv','r',encoding='utf8') as readerFile:
        reader = csv.reader(readerFile)
        for data in reader:
            sentiment_data.append(data)
    return sentiment_data

# Function to train the sentiment analysis model
def model_train():
    sentiment_data = getSentiment_data()
    # Convert the text dataset to DataFrame format
    df = pd.DataFrame(sentiment_data, columns=['text', 'sentiment'])

    # Split the dataset into training and testing sets
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    # Use TF-IDF feature extraction method to convert text data to feature vectors
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(train_data['text'])
    Y_train = train_data['sentiment']
    X_test = vectorizer.transform(test_data['text'])
    Y_test = test_data['sentiment']

    # Train the Naive Bayes classifier
    classifier = MultinomialNB()
    classifier.fit(X_train, Y_train)

    # Predict on the test set
    Y_pred = classifier.predict(X_test)

    # Calculate accuracy
    accuracy = accuracy_score(Y_test, Y_pred)
    print(f"Accuracy: {accuracy}")

    return vectorizer,classifier

# Function for sentiment classification
def sentiment_analysis(text):
    vectorizer, classifier = model_train()
    text_vector = vectorizer.transform([text])
    sentiment = classifier.predict(text_vector)[0]
    return sentiment

if __name__ == "__main__":
    # Test （compare with SnowNLP)
    input_text = "什么破烂玩意？"
    result = sentiment_analysis(input_text)
    print('Result of SnowNLP: ' + str(SnowNLP(input_text).sentiments))
    print('Result of Train Model: ' + result)  # Output: 'positive' but it's obviously negative
