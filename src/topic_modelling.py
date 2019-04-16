import os
import pandas as pd
from gensim import corpora
import gensim
import pickle
from src.data_cleaning import DataPrep

main_path = os.path.dirname(__file__)

print("Running DataPrep class")
data_prep = DataPrep()

data_prep.read_data()
data_prep.parse_document()
data_prep.cleaning_reviews()

 # Create dictionary from reviews then converting to bag-of-words
print("Generating dictionary and corpus")
dictionary = corpora.Dictionary(data_prep.reviews)
corpus = [dictionary.doc2bow(text) for text in data_prep.reviews]

print("Saving dictionary and corpus")
# save dictionary and corpus for future use
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

# Ask LDA model to find 5 topics
print("Running LDA model")
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=4)
for topic in topics:
    print(topic)



