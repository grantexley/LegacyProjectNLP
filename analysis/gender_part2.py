#!/usr/bin/env python3

import pickle
import string
from pprint import pprint
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

PATH = '../entrevistas/'


def get_training_data():
    with open('gender_for_doc.pkl', 'rb') as f:
        gender_per_doc = pickle.load(f)
    
    data = []
    for doc, gender in gender_per_doc.items():
        
        if gender != 'UNKNOWN':
            continue
        
        with open(PATH + doc, "r") as f:
            text = f.read().lower()
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        text = text.replace('\n', ' ')
        
        text = text.replace('¿', ' ')
        
        words = text.split()
        
        words_list = []
        
        while len(words) > 2:
            if words[0] == 'soy' or words[0] == 'estoy':
                words_list.append(words[1] + " " + words[2])
                
            words.pop(0)
            
        data.append((words_list, gender))

    # with open('gender_dataset.pkl', "wb") as f:
    #     pickle.dump(data, f)
    
    return data


def get_new_data():
    with open('gender_for_doc.pkl', 'rb') as f:
        gender_per_doc = pickle.load(f)
    
    data_dict = {}
    for doc, gender in gender_per_doc.items():
        
        if gender != 'UNKNOWN':
            continue
        
        with open(PATH + doc, "r") as f:
            text = f.read().lower()
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        text = text.replace('\n', ' ')
        
        text = text.replace('¿', ' ')
        
        words = text.split()
        
        words_list = []
        
        while len(words) > 2:
            if words[0] == 'soy' or words[0] == 'estoy':
                words_list.append(words[1] + " " + words[2])
                
            words.pop(0)
            
        data_dict[doc] = words_list

    with open('new_gender_dataset.pkl', "wb") as f:
        pickle.dump(data_dict, f)
    
    return data_dict


def main():
    data = get_training_data()
    # with open('gender_dataset.pkl', "rb") as f:
    #     data = pickle.load(f) 
        
    word_lists = [d[0] for d in data]
    labels = [d[1] for d in data]

    # Convert word lists into strings
    word_strings = [' '.join(words) for words in word_lists]

    # Convert words into numerical features
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(word_strings)

    # Step 3: Model Selection and Training
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

    # Choose a classifier (e.g., Naive Bayes) and train the model
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    # Step 4: Evaluation
    # Predict labels for test data
    y_pred = classifier.predict(X_test)

    # Evaluate model performance
    accuracy = accuracy_score(y_test, y_pred)
    
    new_data = get_new_data()
    # with open('new_gender_dataset.pkl', "rb") as f:
    #     new_data = pickle.load(f)
        
    #count = 0
    with open('gender_for_doc.pkl', 'rb') as f:
        gender_dict = pickle.load(f)
        
    for doc, word_list in new_data.items():
        words_string = ' '.join(word_list)
        new_X = vectorizer.transform([words_string])
        prediction = classifier.predict(new_X)
        probabilities = classifier.predict_proba(new_X)
        confidence_level = probabilities[0][np.argmax(prediction)]
        if confidence_level > .499999:
            gender_dict[doc] = str(prediction)[2:-2] + ' (ML)'
            #count += 1
            #print(f"{doc}: Prediction - {prediction}, Confidence Level - {confidence_level}\nWords: {word_list}")
    
    pprint(gender_dict)
    with open('gender_for_doc.pkl', 'wb') as f:
        pickle.dump(gender_dict, f)
    #print(count)
    
    
    
if __name__ == '__main__':
    main()