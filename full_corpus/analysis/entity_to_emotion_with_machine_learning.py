#!/usr/bin/env python3

import os
import pickle
import re
from transformers import pipeline
from collections import defaultdict
from pysentimiento import create_analyzer

PATH = '../entrevistas/'

def process_doc(doc):
    with open(PATH + doc, "r") as f:
        text = f.read().lower()
        
    text = text.replace("\n", " ")
    
    delimiters = ['.', ':']
    pattern = '|'.join(map(re.escape, delimiters))
    text = re.split(pattern, text) 
    return text

def extraction_words():
    word_list = []

    with open("to_extract.txt", "r") as f:
        for line in f:
            word_list.append(line.strip())

    return word_list    


def main():
    extracted_entites = extraction_words()
    #sentiment_analyizer = pipeline("text-classification", model="finiteautomata/beto-sentiment-analysis", tokenizer="finiteautomata/beto-sentiment-analysis")
    sentiment_analyizer = create_analyzer(task="sentiment", lang="es")
    with open('entity_extraction_dict.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)
    
    count = 0
    enities_total_dict = {key: defaultdict(float) for key in extracted_entites}
    entity_counts = {key: 0 for key in extracted_entites}
    for doc, entities in loaded_dict.items():
        for line in process_doc(doc):
            for entity in entities.keys():
                if entity in line:
                    entity_counts[entity] += 1
                    score = sentiment_analyizer.predict(line).probas
                    for key, value in score.items():
                        enities_total_dict[entity][key] += value      
        print(f'{count}: {doc}: processed')
        count += 1
        # if count > 20:
        #     breakh    
   
   
   
    with open('entity_emotions_advanced_extraction.pkl', 'wb') as f:
        pickle.dump(enities_total_dict, f)
        
    with open('counts_of_entity_emotions_advanced_extraction.pkl', 'wb') as f:
        pickle.dump(entity_counts, f)
             
    for entity, scores in enities_total_dict.items():
        total = sum(scores.values())
        print(f'{entity:}:')
        for emotion in enities_total_dict[entity]:
            enities_total_dict[entity][emotion] /= total
            print(f'\t{emotion}:    {enities_total_dict[entity][emotion]}')
            
    print(entity_counts)
    

              
    
            
            
        
            


if __name__ == '__main__':
    main()
    