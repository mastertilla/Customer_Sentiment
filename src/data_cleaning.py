import nltk
import os
import re
from nltk.stem import WordNetLemmatizer
from utils.dataprep import tokenize_text, expand_contractions
import pandas as pd
import datetime
from utils.contractions import CONTRACTION_MAP
import contractions


class DataPrep():
    def __init__(self, data=None):
        self.main_path = os.path.dirname(__file__)
        self.data = None

        if data is None:
            self.data_path = os.path.join(self.main_path, "..", "results", "2019-04-15_trustpilot_reviews.csv")
        else:
            self.data = data

        self.stopwords = nltk.corpus.stopwords.words('english')
        self.lemmatizer = WordNetLemmatizer()

    def read_data(self):
        if self.data is None:
            self.data = pd.read_csv(self.data_path, sep=',')

        # drop duplicate reviews
        self.data.drop_duplicates(subset=['Id'], inplace=True)

    def parse_document(self):
        self.dict_sentences = {}
        for _, row in self.data.iterrows():
            id = row['Id']
            document = re.sub('\n', ' ', row['Review'])
            if isinstance(document, str):
                document = document
            else:
                raise ValueError('Document is not string or unicode!')
            document = document.strip()
            sentences = nltk.sent_tokenize(document)
            self.dict_sentences[id] = sentences
            self.ids = list(self.dict_sentences.keys())

    def clean_reviews(self):
        for _, review_id in enumerate(self.ids):
            for sentences in self.dict_sentences[review_id]:
                print(sentences)
                decontracted_sentence = contractions.fix(sentences)
                # sentences = expand_contractions(self.dict_sentences[review_id], CONTRACTION_MAP)
                sentences = tokenize_text(decontracted_sentence)
                print(sentences)
                # self.dict_sentences[review_id] = sentences

    def do_all(self):
        self.read_data()
        self.parse_document()
        self.clean_reviews()


if __name__ == "__main__":
    data_prep = DataPrep()
    data_prep.read_data()
    data_prep.parse_document()
    data_prep.clean_reviews()

    print(data_prep.dict_sentences)