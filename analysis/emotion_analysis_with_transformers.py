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

def analyze_emotions(substrings, emotion_analysis):

    results = []
    for string in substrings:
        results.append(emotion_analysis(string))
    
    return results


def extract_dict(results):

    combined_emotions = {}
    #creates dict of emotions
    for result in results:
        for emotion in result:
            if emotion['label'] in combined_emotions:
                combined_emotions[emotion['label']] += emotion['score']
            else:
                combined_emotions[emotion['label']] = emotion['score']

    del combined_emotions['others']

    total = sum(combined_emotions.values())

    for key, value in combined_emotions.items():
        combined_emotions[key] = combined_emotions[key] / total

    
    return sorted(combined_emotions.items(), key=lambda item: item[1], reverse=True)



def main():
    
    emotion_analysis = pipeline("text-classification", model="finiteautomata/beto-emotion-analysis", tokenizer="finiteautomata/beto-emotion-analysis")
    
    path = "../entrevistas/"
    docs = sorted(os.listdir(path))

    emotions_dict = {}

    for i, doc in enumerate(docs):

        with open( path + doc, "r") as f:
            text = f.read()
        
        substrings = text_to_substrings(text)

        results = analyze_emotions(substrings, emotion_analysis)

        emotions = extract_dict(results)

        emotions_dict[doc] = emotions

        print(f'processed document {i}: {doc} -- {emotions}')

    with open('emotions_from_transformer_dict.pkl', 'wb') as f:
        pickle.dump(emotions_dict, f)


    

if __name__ == '__main__':
    main()