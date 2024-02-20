#!/usr/bin/env python3

import os
import pandas as pd

directory = "../corpus/"

data_matrix = []
columns = []

for file in os.listdir(directory):
    #check to only modify interviews
    if not file[0].isdigit():
        continue

    path = directory + file
    columns.append(file) #makes list of file names to use as columns in the dataframe

    with open(path, 'r', encoding='utf-8') as in_file:
        text = in_file.read()

    tokens = text.split() #tokenizes file

    #fixes all rows to be the same length (68786 is the length of longest file)
    while len(tokens) != 68786:
        tokens.append("")

    data_matrix.append(tokens)

df = pd.DataFrame(data_matrix)
df = df.T
df.columns = columns

print(df)

df.to_pickle("man3dataframe.pkl")

    

