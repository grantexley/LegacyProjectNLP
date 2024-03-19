#!/usr/bin/env python3

import pickle
import pandas as pd
from collections import defaultdict


def get_enitity_counts(entity_dict):
    result = defaultdict(int)

    for value in entity_dict.values():
        for entity, number in value.items():
            result[entity] += number

    return dict(result)

def main():

    with open('emotions_from_doc_dict.pkl', 'rb') as f:
        emotions_dict = pickle.load(f)

    with open('entity_extraction_dict.pkl', 'rb') as f:
        entity_dict = pickle.load(f)

    entity_counts = get_enitity_counts(entity_dict)

    entity_emotions = defaultdict(lambda: defaultdict(float))

    for doc, value in entity_dict.items():
        for entity, count in value.items():
            for emotion, weight in emotions_dict[doc]:
                entity_emotions[entity][emotion] += count * weight

    for entity, emotions in entity_emotions.items():
        for emotion in emotions.keys():
            entity_emotions[entity][emotion] /= entity_counts[entity]

    for entity, emotions in entity_emotions.items():
        print(f'Entity: {entity}:\n')
        for emotion, weight in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
            print(f'\t{emotion}: {weight}')
        print()
       


if __name__ == '__main__':
    main()