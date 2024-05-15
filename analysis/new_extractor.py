#!/usr/bin/env python3

import os
import re
from collections import defaultdict
from unidecode import unidecode
import pickle
import sys

PATH = "../entrevistas/"

def get_list(extract_file):
    l = []
    for line in open(extract_file, "r"):
        for string in line.rstrip().split("."):
            string = string.strip()
            if string.isupper():
                string = " " + string + " "
            string = unidecode(string)
            l.append(string)
            
    return l
    
def main():
    entity_extraction = False
    
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        extract_file = "violations_to_extract.txt"
        count_file = "violations_count.pkl"
        output_pkl = "violations_extraction_per_doc.pkl"
    else:
        entity_extraction = True
        extract_file = "to_extract.txt"
        count_file = "extracted_counts.pkl"
        output_pkl = "new_entity_extraction.pkl" 

    entities = get_list(extract_file)
    print(entities)
    
    docs = sorted(os.listdir(PATH))
    
    enities_per_doc_dict = {key: defaultdict(int) for key in docs}
    total_entities_count = defaultdict(int)
    
    for doc in docs:
        with open(PATH + doc, "r") as f:
            text = unidecode(f.read().lower())
        
        for entity in entities:
            if entity == ' MAS ':
                matches = re.findall(entity, text)
            else:
                matches = re.findall(entity, text, flags=re.IGNORECASE)
            
            enities_per_doc_dict[doc][entity.strip()] += len(matches)
            total_entities_count[entity.strip()] += len(matches)
        
        print(f'processed: {doc}')
            
    with open(count_file, "wb") as f:
        pickle.dump(total_entities_count, f)    
    
    with open(output_pkl, "wb") as f:
        pickle.dump(enities_per_doc_dict, f)
        
    if entity_extraction:
        with open("actually_extracted.txt", "w") as f:
            for key, val in total_entities_count.items():
                if val > 0:
                    f.write(key.strip() + "\n")
        
        
    #print(sorted(total_entities_count.items(), key=lambda x: x[1], reverse=True))
    #print(enities_per_doc_dict)


            

if __name__ == '__main__':
    main()