#!/usr/bin/env python3

import spacy
import os
import es_dep_news_trf
import sys
import pickle

nlp = spacy.load("es_dep_news_trf")

nlp = es_dep_news_trf.load()

corpus = os.getcwd() + "/../corpus/"

#lemmatizes a string and returns a list of lemmatized words
def lemmatize_doc(string: str) -> list[str]:
    doc = nlp(string)
    return [word.lemma_.split()[0] for word in doc]


def main(arguments=sys.argv):
    #first command line argument is a limit on how many files to process
    try:
        doc_limit = int(arguments[1])
    except:
        doc_limit = None
    
    files = sorted(os.listdir(corpus))

    lemma_dict = {}

    for i, doc in enumerate(files):
        if doc_limit and i >= doc_limit:
            break

        with open(corpus + doc, 'r', encoding='utf-8') as file:
            text = file.read()
        
        lemmatized = lemmatize_doc(text)

        #add lemmatized doc to the dict
        lemma_dict[doc] = lemmatized

        print(f'Document {i}: {doc} Processed')

    #stores dict as a pickle file
    with open('lemmatized_dict.pkl', 'wb') as f:
        pickle.dump(lemma_dict, f)


if __name__ == '__main__':
    main()