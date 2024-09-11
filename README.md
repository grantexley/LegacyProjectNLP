# LegacyProjectNLP

This project is part of a larger project at the University of Notre Dame called [The Legacy Project](https://kroc.nd.edu/research/the-legacy-project/). The Legacy Project at the University of Notre Dame guarentees researches access to a large collection of documents from the Colombian Truth Commission on the Colombian Civil war. 

This repository looks at over 2000 interviews from the Legacy Project, mostly from mandate 3 and extracts meaningful information including the gender of the interviewee, emotion analysis, sentiment analysis, tfidf vectors, topic and entity extraction and more. 



## Usage

The corpus in its raw form exists in the `entrevistas` directory
The preprocessed corpus exists in the `corpus` directory

To run the code in this directory, clone this repository and  install the requirements using `pip -r install requirements.txt`

Then, to create the excel sheet containing all of the analysis on the corpus, run the following commands:
`cd analysis`
`make`

### Acknowledgments

This project was developed in collaboration with Josephine Lechartre. While I was responsible for the coding, she provided guidance and direction throughout the project