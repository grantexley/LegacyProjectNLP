#!/usr/bin/env python3

import os
import pandas as pd
import pickle
import pprint

NOT_IN_DF = set(['517-AA-00001.txt', '235-AA-00002.txt', '246-AA-00001.txt', '240-AA-00006.txt'])

def init_dataframe(file):
    df = pd.read_csv(file)

    save_set = os.listdir("../entrevistas/")

    save_set = set([x[:-4] for x in save_set]) #removes .txt and makes it a set

    filtered_df = df[df['código de la entrevista'].isin(save_set)]

    df = filtered_df.copy()

    df = df.iloc[:, :10]
    df = df.sort_values(by=df.columns[0])
    
    
    # df.loc[len(df)] = ['517-AA-00001'] + ["UNKNOWN"]*9
    # df.loc[len(df)] = ['235-AA-00002'] + ["UNKNOWN"]*9
    # df.loc[len(df)] = ['246-AA-00001'] + ["UNKNOWN"]*9
    # df.loc[len(df)] = ['240-AA-00006'] + ["UNKNOWN"]*9


    return df

def add_emotions(df, dictionary, prefix):
    emotion1 = []
    emotion1weight = []
    emotion2 = []
    emotion2weight = []
    emotion3 = []
    emotion3weight = []

    for key, value in dictionary.items():
        if key in NOT_IN_DF:
            continue
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

def extraction_words(text_file):
    word_list = []

    with open(text_file, "r") as f:
        for line in f:
            word_list.append(line.strip())

    return word_list

def add_entity_extraction(df, dictionary, text_file):
    extraction_word_list = extraction_words(text_file)

    for word in extraction_word_list:
        word_list = []
        for doc in sorted(os.listdir("../entrevistas/")):
            if doc in NOT_IN_DF:
                continue
            if word in dictionary[doc]:
                word_list.append(dictionary[doc][word])
            else:
                word_list.append(0)
                
        df[word] = word_list


def add_tfidf(df, dictionary):
    to_add = [ [] for _ in range(15) ]
    for doc, words_dict in dictionary.items():
        if doc in NOT_IN_DF:
            continue
        
        for index, (word, score) in enumerate(words_dict):
            to_add[index].append(f'{word} ({score:.3})')
            
    for i, l in enumerate(to_add):
        df["tfidf word " + str(i+1)] = l
        
def add_sentiment(df, dictionary):
    
    NEG = []
    NEU = []
    POS = []
    
    for doc, sent_dict in dictionary.items():
        if doc in NOT_IN_DF:
            continue
        
        for sentiment, score in sent_dict.items():
            if sentiment == 'NEG':
                NEG.append(score)
            elif sentiment == 'NEU':
                NEU.append(score)
            elif sentiment == 'POS':
                POS.append(score)
            else:
                raise ValueError
    
    df["sent-anal NEG"] = NEG
    df["sent-anal NEU"] = NEU
    df["sent-anal POS"] = POS

def add_sentiment_to_entity(df, sent_dictionary, ent_dictionary):
    
    to_add = [ [] for _ in range(5) ] 
    
    for doc, entities_dict in sent_dictionary.items():
        if doc in NOT_IN_DF:
            continue
        entities = sorted(ent_dictionary[doc].items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (ent, count) in enumerate(entities):
            if count == 0:
                entities[i] = ('None', 0)
                
        for i, (ent, count) in enumerate(entities):
            if ent == 'None':
                to_add[i].append("No Entities Found")
            else:
                to_add[i].append(f'{ent}: ({entities_dict[ent]['NEG']:.3}, {entities_dict[ent]['NEU']:.3}, {entities_dict[ent]['POS']:.3})')
                
                
    for i, l in enumerate(to_add):
        df[f'sentiment for entity {i+1}: (NEG, NEU, POS)'] = l
              
        

def main():
    df = init_dataframe('Relacion_Entrevistas_CEV_CSV.csv')
    
    with open('gender_for_doc.pkl', 'rb') as f:
        gender_dict = pickle.load(f)
        
    df['Gender'] = [ gender for doc, gender in gender_dict.items() if doc not in NOT_IN_DF ]

    with open('emotions_from_doc_dict.pkl', 'rb') as f:
        doc_dict = pickle.load(f)
    
    with open('emotions_from_transformer_dict.pkl', 'rb') as f:
        transformer_dict = pickle.load(f)

    add_emotions(df, transformer_dict, "ML")
    add_emotions(df, doc_dict, "lexicon")
    
    with open('emotions_from_transformer_dict.pkl', 'rb') as f:
        transformer_dict = pickle.load(f)
    
    with open('tfidf_scores.pkl', 'rb') as f:
        tdidf_dict = pickle.load(f) 
    
    add_tfidf(df, tdidf_dict)
    
    with open('sentiment_per_doc.pkl', 'rb') as f:
        sentiment_dict = pickle.load(f) 
    
    add_sentiment(df, sentiment_dict)
    
    with open('entity_emotions_document_level.pkl', 'rb') as f:
        sentiment_to_entity_dict = pickle.load(f)
        
    with open('new_entity_extraction.pkl', 'rb') as f:
        entity_extraction_dict = pickle.load(f)

    add_sentiment_to_entity(df, sentiment_to_entity_dict, entity_extraction_dict)
    
    add_entity_extraction(df, entity_extraction_dict, "actually_extracted.txt")

    with open('violations_extraction_per_doc.pkl', 'rb') as f:
        violation_extraction = pickle.load(f)
        
    add_entity_extraction(df, violation_extraction, 'violations_to_extract.txt')

    print(df)

    df.to_excel('interviews_analysis.xlsx', index=False)



if __name__ == '__main__':
    main()