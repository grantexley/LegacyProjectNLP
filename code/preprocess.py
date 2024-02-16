#!/usr/bin/env python3

import os
import pandas as pd
from spanish_nlp import preprocess

directory = "../corpus2/"

sp = preprocess.SpanishPreprocess(
        lower=False,
        normalize_breaklines=True,
        remove_vowels_accents=True,
        remove_multiple_spaces=True,
        remove_punctuation=True,
        remove_unprintable=True,
        remove_numbers=False,
        remove_stopwords=True,
        stopwords_list="default",
        lemmatize=False,
        stem=False,
)

# Iterate through each file in the directory
for file in os.listdir(directory):
    if not file[0].isdigit():
        continue

    path = directory + file
    
    # Read the contents of the file
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    #modify text
    preprocessed_text = sp.transform(text)
    
    #write to file
    with open(path, 'w', encoding='utf-8') as output_file:
        output_file.write(preprocessed_text)

    print(f"Preprocessed {path}")