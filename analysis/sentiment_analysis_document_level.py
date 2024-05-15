#!/usr/bin/env python3

import os
import pickle
from collections import defaultdict
from pysentimiento import create_analyzer

PATH = '../entrevistas/'




def main():

    docs = sorted(os.listdir(PATH))

    sentiment_analyizer = create_analyzer(task="sentiment", lang="es")
    
    sentiment_per_doc = {key: defaultdict(float) for key in docs}

    for i, doc in enumerate(docs):

        with open( PATH + doc, "r") as f:
            text = f.read()
        
        score = sentiment_analyizer.predict(text).probas
        
        for key, value in score.items():
            sentiment_per_doc[doc][key] += value 
        
        print(f'processed document {i}: {doc} {score}')
        
        # if i > 20:
        #     break
    
    #print(sentiment_per_doc)

    with open('sentiment_per_doc.pkl', 'wb') as f:
        pickle.dump(sentiment_per_doc, f)


    

if __name__ == '__main__':
    main()