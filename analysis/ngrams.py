#!/usr/bin/env python3

import pickle

#opens lemmatized dict file
with open('lemmatized_dict.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

ngram_dict = {}

#creates bigram for each doc in the dict of lemmatized docs
for key, value in loaded_dict.items():
    doc = []
    for i in range(len(value)-1):
        doc.append((value[i], value[i+1]))
    ngram_dict[key] = doc

#saves new pickle file
with open('bi-grams.pkl', 'wb') as f:
    pickle.dump(ngram_dict, f)


