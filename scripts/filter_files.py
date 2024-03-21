#!/usr/bin/env python3

import os

man3 = {}
#adds all the names of the files in mandate 3 into a dict
with open("files_in_corpus.txt", 'r') as file:
    for line in file:
        man3[line.strip() + ".pdf"] = 0

#list of all files in the entrevistas directory
ls = os.listdir("../entrevistas")

#removes every file in entrevistas directory not in mandate 3
for file in ls:
    if not file in man3:
        os.remove("../entrevistas/" + file)
