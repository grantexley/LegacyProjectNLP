#!/usr/bin/env python3


import os
import pickle

def extraction_words():
    word_list = []

    with open("to_extract.txt", "r") as f:
        for line in f:
            word_list.append(line.strip())

    return word_list    

def main():

    extraction_dict = {}

    words_to_extract = extraction_words()

    with open('lemmatized_dict.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    count = 0
    for doc, words in loaded_dict.items():
        print(f'processed {doc}')
        # count += 1
        # if count > 6:
        #     break
        extraction_dict[doc] = {}
        for word in words:
            if word in words_to_extract:
                if word in extraction_dict[doc]:
                    extraction_dict[doc][word] += 1
                else:
                    extraction_dict[doc][word] = 1
        print(f'processed {doc}')
    with open('entity_extraction_dict.pkl', 'wb') as f:
        pickle.dump(extraction_dict, f)




if __name__ == '__main__':
    main()