
SOURCES= dataframe.py Relacion_Entrevistas_CEV_CSV.csv gender_for_doc.pkl emotions_from_doc_dict.pkl emotions_from_transformer_dict.pkl tfidf_scores.pkl sentiment_per_doc.pkl entity_emotions_document_level.pkl new_entity_extraction.pkl actually_extracted.txt violations_extraction_per_doc.pkl violations_to_extract.txt 


interviews_analysis.xlsx: 	$(SOURCES)
	./dataframe.py


gender_for_doc.pkl:		gender_part1.py gender_part2.py
	./gender_part1.py
	./gender_part2.py


emotions_from_doc_dict.pkl:		emotion_analysis_with_doc_and_negation.py lexicon_afectivo_categorias.csv
	./emotion_analysis_with_doc_and_negation.py


emotions_from_transformer_dict.pkl: 	emotion_analysis_with_transformers.py
	./emotion_analysis_with_transformers.py


tfidf_scores.pkl: 	tfidf.py lemmatized_dict.pkl tfidf_remove.txt
	./tfidf.py


sentiment_per_doc.pkl:		sentiment_analysis_document_level.py
	./sentiment_analysis_document_level.py


entity_emotions_document_level.pkl:		entity_to_emotion_with_machine_learning_document_level.py actually_extracted.txt new_entity_extraction.pkl
	./entity_to_emotion_with_machine_learning_document_level.py


new_entity_extraction.pkl extracted_counts.pkl actually_extracted.txt:		new_extractor.py to_extract.txt
	./new_extractor.py


violations_extraction_per_doc.pkl:		new_extractor.py violations_to_extract.txt
	./new_extractor.py -v