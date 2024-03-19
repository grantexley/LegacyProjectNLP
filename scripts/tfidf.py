#!/usr/bin/env python3

from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import sys



def get_documents():
    with open('lemmatized_dict.pkl', 'rb') as f:
        data = pickle.load(f)

    #turns list of tokens into a string
    return data, [" ".join(tokens) for tokens in data.values()]
    

def entire_corpus_graph(tfidf_matrix, feature_names, num_tokens):

    total_tfidf_scores = tfidf_matrix.sum(axis=0).A1
    total_tfidf_scores_dict = {feature_names[i]: total_tfidf_scores[i] for i in range(len(feature_names))}

    #sort tokens by TF-IDF score in descending order
    sorted_tokens = sorted(total_tfidf_scores_dict.items(), key=lambda x: x[1], reverse=True)

    #plot the TF-IDF scores
    plt.figure(figsize=(10, 6))
    top_tokens = [token for token, score in sorted_tokens[:num_tokens]]
    top_scores = [score for token, score in sorted_tokens[:num_tokens]]
    plt.barh(range(len(top_tokens)), top_scores, align='center')
    plt.yticks(range(len(top_tokens)), top_tokens)
    plt.xlabel('TF-IDF Score')
    plt.ylabel('Token')
    plt.title(f'Top {num_tokens} Tokens by TF-IDF Score')
    plt.show()

    #creates a table for the TF-IDF scores
    tfidf_table = pd.DataFrame(sorted_tokens, columns=['Token', 'TF-IDF Score'])
    print(tfidf_table.head(num_tokens))


def single_doc_graph(doc_name, data, tfidf_matrix, feature_names, num_tokens):
    # Check if the document exists in the data dictionary
    if doc_name not in data:
        print("Document not found!")
        return

    #get the index of the document in the data dictionary
    doc_index = list(data.keys()).index(doc_name)

    #extract TF-IDF scores for the specified document
    tfidf_scores = tfidf_matrix[doc_index].toarray().flatten()

    #create a dictionary with tokens and their TF-IDF scores
    token_tfidf_scores = {feature_names[j]: tfidf_scores[j] for j in range(len(feature_names)) if tfidf_scores[j] != 0}

    #sort tokens by TF-IDF score in descending order
    sorted_tokens = sorted(token_tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:num_tokens]

    #plot the TF-IDF scores
    plt.figure(figsize=(8, 6))
    plt.barh(range(len(sorted_tokens)), [score for token, score in sorted_tokens], align='center')
    plt.yticks(range(len(sorted_tokens)), [token for token, score in sorted_tokens])
    plt.xlabel('TF-IDF Score')
    plt.ylabel('Token')
    plt.title(f'Top {num_tokens} TF-IDF Scores for ' + doc_name)
    plt.show()

    tfidf_table = pd.DataFrame(sorted_tokens, columns=['Token', 'TF-IDF Score'])
    print(tfidf_table.head(num_tokens))



def main(arguments=sys.argv[1:]):

    data, documents = get_documents()

    tfidf_vectorizer = TfidfVectorizer()

    #computes the TF-IDF values
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

    #gets tokens from the vectorizer
    feature_names = tfidf_vectorizer.get_feature_names_out()


    if not arguments: #no arguments 
        entire_corpus_graph(tfidf_matrix, feature_names, 30)
        return 0

    try: #option 1: user enters a number first, so we show the full corpus
        num_tokens = int(arguments[0])
    except: #option 2: user enters in a file first, so we show TF-IDF for that document
        try:
            num_tokens = int(arguments[1])
        except:
            num_tokens = 20

        single_doc_graph(arguments[0], data, tfidf_matrix, feature_names, num_tokens)
    else:
        entire_corpus_graph(tfidf_matrix, feature_names, num_tokens)


if __name__ == '__main__':
    main()