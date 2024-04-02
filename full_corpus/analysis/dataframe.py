#!/usr/bin/env python3

import os
import pandas as pd
import pickle


def init_dataframe(file):
    df = pd.read_csv(file)

    save_set = os.listdir("../entrevistas/")

    save_set = set([x[:-4] for x in save_set]) #removes .txt and makes it a set
    
    filtered_df = df[df['código de la entrevista'].isin(save_set)]

    df = filtered_df.copy()

    df = df.iloc[:, :10]
    df = df.sort_values(by=df.columns[0])

    return df

def add_emotions(df, dictionary, prefix):
    emotion1 = []
    emotion1weight = []
    emotion2 = []
    emotion2weight = []
    emotion3 = []
    emotion3weight = []

    for key, value in dictionary.items():
        if len(value) == 1:
            value.append(('none', 0.0))
        if len(value) == 2:
            value.append(('none', 0.0))
        emotion1.append(value[0][0])
        emotion1weight.append(value[0][1])
        emotion2.append(value[1][0])
        emotion2weight.append(value[1][1])
        emotion3.append(value[2][0])
        emotion3weight.append(value[2][1])

    df[ prefix + '-emotion1' ] = emotion1
    df[ prefix + '-emotion1-weight' ] = emotion1weight
    df[ prefix + '-emotion2' ] = emotion2
    df[ prefix + '-emotion2-weight' ] = emotion2weight
    df[ prefix + '-emotion3' ] = emotion3
    df[ prefix + '-emotion3-weight' ] = emotion3weight

def extraction_words():
    word_list = []

    with open("to_extract.txt", "r") as f:
        for line in f:
            word_list.append(line.strip())

    return word_list

def add_entity_extraction(df, dictionary):
    extraction_word_list = extraction_words()

    for word in extraction_word_list:
        word_list = []
        for doc in sorted(os.listdir("../corpus/")):
            if word in dictionary[doc]:
                word_list.append(dictionary[doc][word])
            else:
                word_list.append(0)
                
        df[word] = word_list



def main():
    df = init_dataframe('Relacion_Entrevistas_CEV_CSV.csv')

    with open('emotions_from_doc_dict.pkl', 'rb') as f:
        doc_dict = pickle.load(f)
    
    with open('emotions_from_transformer_dict.pkl', 'rb') as f:
        transformer_dict = pickle.load(f)

    add_emotions(df, transformer_dict, "spacy")
    add_emotions(df, doc_dict, "tc")

    with open('entity_extraction_dict.pkl', 'rb') as f:
        entity_extraction_dict = pickle.load(f)

    add_entity_extraction(df, entity_extraction_dict)

    df = df.iloc[:-39]

    print(df)

    df.to_excel('man3_dataframe_no_dups.xlsx', index=False)



if __name__ == '__main__':
    main()