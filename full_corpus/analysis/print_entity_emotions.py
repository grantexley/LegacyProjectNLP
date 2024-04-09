#!/usr/bin/env python3

import pickle
from collections import defaultdict


def with_neutral(loaded_dict):
    for entity, scores in loaded_dict.items():
            total = sum(scores.values())
            print(f'{entity:}:')
            print(f'\tPOS:    {loaded_dict[entity]['POS']/total}')
            print(f'\tNEU:    {loaded_dict[entity]['NEU']/total}')
            print(f'\tNEG:    {loaded_dict[entity]['NEG']/total}')
            print()
            
def without_neutral(loaded_dict):
    for entity, scores in loaded_dict.items():
            del loaded_dict[entity]['NEU']
            total = sum(scores.values())
            print(f'{entity:}:')
            print(f'\tPOS:    {loaded_dict[entity]['POS']/total}')
            print(f'\tNEG:    {loaded_dict[entity]['NEG']/total}')
            print()
            

def main():

    with open('entity_emotions_advanced_extraction.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)
        
    with_neutral(loaded_dict)
    without_neutral(loaded_dict)


if __name__ == '__main__':
    main()