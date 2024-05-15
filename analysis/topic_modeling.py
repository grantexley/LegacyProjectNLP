#!/usr/bin/env python3



import pickle
from pprint import pprint
from gensim import corpora
from gensim.models import LdaModel
import re    
from gensim.models import Phrases
import os

def get_documents():
    
    with open('lemmatized_dict.pkl', 'rb') as f:
        data = pickle.load(f)
   
    with open("tfidf_remove.txt", "r") as f:
        remove_set = set([word.strip() for word in f.read().strip().split(",")])     

    for key, value in data.items():
        value = [re.sub(r'\b19\b', 'M-19', s) for s in value if s not in remove_set]
        data[key] = [word for word in value if word not in remove_set and word != 'm-M-19' ]

    #turns list of tokens into a string
    return list(data.values())
    

    
def main():

    docs = get_documents()

    print('grant 0')

    # Add bigrams and trigrams to docs (only ones that appear 20 times or more).
    bigram = Phrases(docs, min_count=20)
    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
                
    print('grant 1')
    
    # Creating document-term matrix 
    dictionary = corpora.Dictionary(docs)
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    
    for i in corpus:
        for j in i:
            if j == "obviamente":
                print('YES') 
    
    # Set training parameters.
    # num_topics = 10
    # chunksize = 2000
    # passes = 10
    # iterations = 50
    # eval_every = None  # Don't evaluate model perplexity, takes too much time.
    
    num_topics = 15
    chunksize = 2000
    passes = 20
    iterations = 400
    eval_every = None

# Make an index to word dictionary.
    temp = dictionary[0]  # This is only to "load" the dictionary.
    id2word = dictionary.id2token
    print('grant 2')
    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )
    print('grant 3')
    top_topics = model.top_topics(corpus)
    
    with open("topics.txt", "w") as f:
        for i, topic in enumerate(top_topics):
            print(f'topic: {i}:\n', file=f)
            pprint(topic, stream=f)
            print(file=f)
        
    
    
    output = {}
    
    for i, doc in enumerate(sorted(os.listdir("../corpus/"))):
        output[doc] = sorted(model.get_document_topics(corpus[i]), key=lambda x: x[1], reverse=True)
    
    with open("document_topics.txt", "w") as f:
        pprint(output, stream=f)
        
        
        
     


if __name__ == '__main__':
    main()