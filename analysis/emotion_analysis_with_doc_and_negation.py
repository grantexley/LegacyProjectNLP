#!/usr/bin/env python3

from unidecode import unidecode
import os
import pickle
import math
from collections import defaultdict
import re

def get_dict():

    remove_set = set(["llevar","llegar","empezar","decir","pa","entender","quedar","tenia","tener","aca","ir","alla","llamar","jue","ay","tonces","ee","ver","eee","ahorita","mjm","aja","oiga","mire","osea","año","venir","eh","dar","uste","gente","er","pausa","ud","err","em","ininteligible","mm","hmm","hm","erm","ok","mirar","persona","onde","dud","ah","entoes","toa","cres","sales","tipo","algun","alguno","alguna","test","ent","llover","poner","exatamente","pu","hablar","to","he","entoces","enton","cosa","fulano","contar","ehh","vea","don","tema","decía","okey","okay"])

    temp = [] 
    emotion_reference = {}
    with open("lexicon_afectivo_categorias.csv", "r") as f:
        count = 0
        for i, line in enumerate(f):
            if count == 0:
                count += 1
                continue

            if "oh, mierda " in line:
                line = line[4:]

            text = line.strip().split(",")
            text = [word.strip() for word in text]
            if text[0] in remove_set:
                continue
            text = [unidecode(x).lower() for x in text if x]
            if len(text) > 1:
                temp.append(text)

            count+=1

    for i, l in enumerate(temp):
        if len(l) > 2 and l[1] == l[2]:
            temp[i] = l[1:3]


    for l in temp:
        if len(l) == 2:
            if l[0] not in emotion_reference:
                emotion_reference[l[0]] = [l[1]]
            elif l[1] not in emotion_reference[l[0]]:
                emotion_reference[l[0]].append(l[1])
        elif len(l) == 3:
            if l[0] not in emotion_reference:
                emotion_reference[l[0]] = [l[1], l[2]]
            else:
                if l[1] not in emotion_reference[l[0]]:
                    emotion_reference[l[0]].append(l[1])
                elif l[2] not in emotion_reference[l[0]]:
                    emotion_reference[l[0]].append(l[2])

    return emotion_reference


def normalize_and_sort_dict(dictionary, emotion_counts):

    total_count = sum([count for count in emotion_counts.values()])

    if "expectativa" in dictionary:
        del dictionary["expectativa"]
        
    
    for key, value in emotion_counts.items():
        if key in dictionary:
            dictionary[key] = (dictionary[key] / emotion_counts[key]) / total_count
            
    total = sum([x for x in dictionary.values()])
    for key, value in dictionary.items():
        dictionary[key] = dictionary[key] / total

    return sorted(dictionary.items(), key=lambda item: item[1], reverse=True)

def count_emotion_prevalence(emotion_reference):
    #count_dict = {"alegria": 0, "tristeza": 0, "enojo": 0, "sorpresa": 0, "miedo": 0, "confianza": 0, "repulsion": 0, "disgusto": 0, "expectativa": 0}
    count_dict = defaultdict(int)
    for key, value in emotion_reference.items():
        for emotion in value:
            count_dict[emotion] += 1

    return count_dict

def tokenize(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.split()
    text = [unidecode(word.lower()) for word in text if not word.isdigit()]
    return text
    


def main():
    
    emotion_reference = get_dict()

    emotion_counts = count_emotion_prevalence(emotion_reference)
    
    path = "../entrevistas/"

    emotions_dict = {}
    
    negation_set = set(["no", "nunca", "jamás", "tampoco", "ni", "ningún", "ninguna", "nadie", "nada", "siquiera", "sin"])

    for doc in sorted(os.listdir(path)):
        
        with open(path + doc) as f:
            text = f.read()
        value = tokenize(text)
        doc_dict = defaultdict(int)
        for index, word in enumerate(value):
            if word in emotion_reference:
                for emotion in emotion_reference[word]:
                    if any(val in negation_set for val in value[ max(0, index - 10) : min(index + 11, len(value) - 1)]):
                        #doc_dict["negated-" + emotion] += 1
                        doc_dict[emotion] -= 1  
                    else:
                        doc_dict[emotion] += 1 

                        
        emotions_dict[doc ] = normalize_and_sort_dict(doc_dict, emotion_counts)
        print(doc + ":")
        print("-------------------")
        for emotion, score in emotions_dict[doc]:
            print(emotion + ":", f'{score:.5}')
        print("\n") 

    

    with open('emotions_from_doc_dict.pkl', 'wb') as f:
        pickle.dump(emotions_dict, f)




if __name__ == '__main__':
    main()
