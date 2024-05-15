#!/usr/bin/env python3


import random
import os
from collections import defaultdict, Counter
import re
from time import sleep
import string
from pprint import pprint
import pickle

def main():
    
    female_words = set(['señora', 'doña' ,'doctora'])
    male_words = set(['don','señor', 'doctor'])
    
    PATH = '../entrevistas/'

    ls = os.listdir(PATH)
    
    # choice = random.choice(ls)
    # with open(PATH + choice, "r") as f:
    #     text = f.read()
    #     beginning = text.split()
    #     try:
    #         beginning = text[text.index("ENT") : text.index("TEST:")].split()
    #     except:
    #         try:
    #             beginning = text[text.index("ENT") : 1000].split()
    #         except:
    #             beginning = text[0 : 1000].split() 

    # print(text[:2000])
    # # print('----------------------------------------')
    # print(beginning)
    
    gender_dict = {}
    
    before_list = []
    male_flag = 0
    female_flag = 0
    count = 0
    word_used = []
    for doc in sorted(os.listdir(PATH)):

        with open(PATH + doc, "r") as f:
            text = f.read().lower()
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        text = text.replace('\n', ' ')
        
        text = text.replace('¿', ' ')
        
        words = text.split()
        
        while (len(words) > 2):
            
            if words[-1] == 'test':
                if words[-2] in female_words:
                    gender_dict[doc] = "female"
                    word_used.append(words[-2])
                    female_flag = 1
                    words.pop()
                elif words[-2] in male_words:
                    male_flag = 1
                    gender_dict[doc] = "male"
                    word_used.append(words[-2])
                    words.pop()

                
                before_list.append(words[-2])

            words.pop()
        
        if doc not in gender_dict:
            gender_dict[doc] = "UNKNOWN"
        # if male_flag or female_flag:
        #     print(f'doc = {doc}')
        #     print(f'male_flag = {male_flag}')
        #     print(f'female_flag = {female_flag}')
        #     print(f'word_used = {word_used}')
        #     os.system("code " + PATH + doc)
        #     input()
            
        # male_flag = 0
        # female_flag = 0
        # word_used = []
        
  
        
        print(f'{doc} processed')
        
    print('-----------------------------------------------------------------------')
    pprint(gender_dict)
    # counts = Counter(sorted(before_list))
    # for word in male_words:
    #     print(word, counts[word])
    # for word in female_words:
    #     print(word, counts[word])
    
    print('female = ', sum ([1 for gender in gender_dict.values() if gender == 'female' ] ))
    print('male = ', sum ([1 for gender in gender_dict.values() if gender == 'male' ] ))
    print('UNKNOWN = ', sum ([1 for gender in gender_dict.values() if gender == 'UNKNOWN' ] ))
        
    with open('gender_for_doc.pkl', "wb") as f:
        pickle.dump(gender_dict, f)
        
    
    
if __name__ == '__main__':
    main()
    
    
    
        # if "TEST1" in text:
        #     continue
        
        # just_ent = re.findall(r'ent:.*?test:', text, re.DOTALL)
        
        # print(just_ent)
            
        # os.system("code " + PATH + doc)
        