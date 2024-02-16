#!/usr/bin/env python3

import os

#path to directory of pdf files
corpus = "../entrevistas/"

#converts every file in the directory to .txt file
ls = os.listdir(corpus)
for file in ls:
    os.system("pdftotext " + corpus + file + " " + corpus + file[:-3] + "txt")

#removes all pdf files
ls = os.listdir(corpus)
for file in ls:
    if file[-3:] == "pdf":
        os.remove(corpus + file)