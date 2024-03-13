#!/usr/bin/env python3

from unidecode import unidecode
import os
import pickle

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

    for key, value in emotion_counts.items():
        if key in dictionary:
            dictionary[key] *= 1 / (emotion_counts[key] / total_count)

    total = sum([x for x in dictionary.values()])
    for key, value in dictionary.items():
        dictionary[key] = dictionary[key] / total

    return sorted(dictionary.items(), key=lambda item: item[1], reverse=True)

def count_emotion_prevalence(emotion_reference):
    count_dict = {"alegria": 0, "tristeza": 0, "enojo": 0, "sorpresa": 0, "miedo": 0, "confianza": 0, "repulsion": 0, "disgusto": 0, "expectativa": 0}

    for key, value in emotion_reference.items():
        for emotion in value:
            if emotion in count_dict:
                count_dict[emotion] += 1
            else:
                print(key, emotion)

    return count_dict


def main():
    
    emotion_reference = get_dict()

    emotion_counts = count_emotion_prevalence(emotion_reference)

    
    path = "../corpus/"

    emotions_dict = {}

    with open('lemmatized_dict.pkl', 'rb') as f:
        loaded_dict = pickle.load(f)

    for key, value in loaded_dict.items():
        doc_dict = {}
        for word in value:
            if word in emotion_reference:
                for emotion in emotion_reference[word]:
                    if emotion in doc_dict:
                        doc_dict[emotion] += 1
                    else:
                        doc_dict[emotion] = 1
        emotions_dict[key] = normalize_and_sort_dict(doc_dict, emotion_counts)
    
    with open('emotions_from_doc_dict.pkl', 'wb') as f:
        pickle.dump(emotions_dict, f)




if __name__ == '__main__':
    main()