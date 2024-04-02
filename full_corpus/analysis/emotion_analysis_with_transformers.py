#!/usr/bin/env python3

from transformers import pipeline
import os
import pickle


#since the emotion analyzer can only process 512 characters at a time, we need to seperate the text string into substrings
def text_to_substrings(text):
    substrings = []

    substring = ""
    for word in text.split():
        if len(substring) + len(word) < 512:
            substring += word + " " 
        else:
            substrings.append(substring)
            substring = ""

    return substrings

def analyze_emotions(substrings):
    emotion_analysis = pipeline("text-classification", model="finiteautomata/beto-sentiment-analysis", tokenizer="finiteautomata/beto-sentiment-analysis")

    results = []
    for string in substrings:
        results.append(emotion_analysis(string))
    
    return results


def extract_dict(results):
    
    combined_emotions = {'NEG': 0, 'NEU': 0, 'POS': 0}
    #creates dict of emotions
    for result in results:
        for sentiment in result:
            combined_emotions[sentiment['label']] += sentiment['score']

    total = sum(combined_emotions.values())

    for key in combined_emotions.keys():
        combined_emotions[key] = combined_emotions[key] / total

    
    return combined_emotions.items()



def main():
    path = "../entrevistas/"
    docs = sorted(os.listdir(path))

    emotions_dict = {}

    for i, doc in enumerate(docs):

        with open( path + doc, "r") as f:
            text = f.read()
        
        substrings = text_to_substrings(text)

        results = analyze_emotions(substrings)

        emotions = extract_dict(results)
        
        # emotions_dict[doc] = emotions
        
        with open("sentiment.txt", "a") as f:
            print(f'{doc}: {emotions}', file=f)
        
        print(f'processed document {i}: {doc} {emotions}')

    # with open('emotions_from_transformer_dict.pkl', 'wb') as f:
    #     pickle.dump(emotions_dict, f)


    

if __name__ == '__main__':
    main()