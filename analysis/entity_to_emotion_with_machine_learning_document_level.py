#!/usr/bin/env python3

import os
import pickle
import re
from transformers import pipeline
from collections import defaultdict
from pysentimiento import create_analyzer
import pprint
from unidecode import unidecode

PATH = '../entrevistas/'

def process_doc(doc):
    with open(PATH + doc, "r") as f:
        text = f.read().lower()
        
    text = text.replace("\n", " ")
    
    delimiters = ['.', ':']
    pattern = '|'.join(map(re.escape, delimiters))
    text = re.split(pattern, text) 
    return [unidecode(t) for t in text]

def extraction_words():
    word_list = []

    with open("actually_extracted.txt", "r") as f:
        for line in f:
            word_list.append(line.strip())

    return word_list    


def main():
    extracted_entites = extraction_words()
    #sentiment_analyizer = pipeline("text-classification", model="finiteautomata/beto-sentiment-analysis", tokenizer="finiteautomata/beto-sentiment-analysis")
    
    docs = sorted(os.listdir(PATH))
    
    sentiment_analyizer = create_analyzer(task="sentiment", lang="es")
    
    with open('new_entity_extraction.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)
    
    #pprint.pprint(loaded_dict)
    
    enities_emotion = {}
    
    for doc in docs:
        enities_emotion[doc] = {}
        for entity in extracted_entites:
            if loaded_dict[doc][entity] != 0:
                enities_emotion[doc][entity] = defaultdict(float)

    # pprint.pprint(enities_emotion['001-PR-00679.txt'])
    
    count = 0
    
    
    for doc, entity_dict in enities_emotion.items():
        for line in process_doc(doc):
            for entity in entity_dict.keys():
                if entity.isupper():
                    entity = " " + entity + " "
                if (re.findall(entity, line, re.IGNORECASE)):
                    entity = entity.strip()
                    score = sentiment_analyizer.predict(line).probas 
                    for sent, num in score.items():
                        enities_emotion[doc][entity][sent] += num
                          
        count += 1
        print(f'{count}: processed {doc}')
        # if count > 0:
        #     break    

    for doc, entity_dict in enities_emotion.items():
        #print(f'DOC: --- {doc} --- ')
        for entity in entity_dict.keys():
            total = sum(entity_dict[entity].values())
            #print(f'\t{entity:}:')
            for sentiment in entity_dict[entity]:
                enities_emotion[doc][entity][sentiment] /= total
                #print(f'\t\t{sentiment}:    {enities_emotion[doc][entity][sentiment]}')
                
   
    with open('entity_emotions_document_level.pkl', 'wb') as f:
        pickle.dump(enities_emotion, f)
        

    

              
    
            
            
        
            


if __name__ == '__main__':
    main()
    