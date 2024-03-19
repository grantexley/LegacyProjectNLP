#!/usr/bin/env python3

import spacy
import os
from multiprocessing import Pool, cpu_count

nlp = spacy.load('es_core_news_sm')

def extract_entities_from_document(document):
    doc = nlp(document)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

def process_file(doc):
    path = "../corpus/"
    with open(path + doc, "r") as f:
        text = f.read()

    entities = extract_entities_from_document(text)

    with open("named_extraction.txt", "a") as output_file:
        for entity, label in entities:
            output_file.write(entity + "\n")

    print(f"Processed file: {doc}")

def main():
    path = "../corpus/"
    ls = sorted(os.listdir(path))

    # Determine the number of processes to use
    num_processes = min(cpu_count(), len(ls))
    print(num_processes)

    # Create a pool of worker processes
    with Pool(num_processes) as pool:
        pool.map(process_file, ls)

    

if __name__ == '__main__':
    main()