#!/usr/bin/env python3

import os
from spanish_nlp import preprocess

directory = "../corpus/"

sp = preprocess.SpanishPreprocess(
        lower=False,
        normalize_breaklines=True,
        remove_vowels_accents=True,
        remove_multiple_spaces=True,
        remove_punctuation=True,
        remove_unprintable=True,
        remove_numbers=True,
        remove_stopwords=True,
        stopwords_list="extended",
        lemmatize=False,
        stem=False,
)


# Iterate through each file in the directory

def additionall_filter(text, save_set, delete_set):
    index = 0
    text = text.split()
    while index < len(text):
        word = text[index]
        if word == 'M':
            text[index] = "M-19"
            index += 1
        elif word.isupper() and word not in save_set:
            text.pop(index)
        elif word in delete_set or all(char == 'x' for char in word):
            text.pop(index)
        else:
            index += 1

    return " ".join(text).lower()


def main():
    save_set = set()
    with open("capital_keep.txt", 'r') as file:
        for word in file:
            save_set.add(word.strip())

    delete_set = set(["entonces", "sin embargo", "donde", "el", "ella", "si", "tambien", "vale", "ok", "ent"])
    
    for file in os.listdir(directory):
        if not file[0].isdigit():
            continue

        path = directory + file

        # Read the contents of the file
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()

        #modify text
        preprocessed_text = sp.transform(text)

        preprocessed_text = additionall_filter(preprocessed_text, save_set, delete_set)
        
        #write to file
        with open(path, 'w', encoding='utf-8') as output_file:
            output_file.write(preprocessed_text)

        print(f"Preprocessed {path}")


if __name__ == '__main__':
    main()