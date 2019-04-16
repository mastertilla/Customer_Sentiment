import nltk
import os
import re
from nltk.stem import WordNetLemmatizer
import string
import pandas as pd
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

        self.dict_sentences = None
        self.dict_sentences = {}
        self.individual_sentences = {}

        self.reviews = []

    def read_data(self):
        if self.data is None:
            self.data = pd.read_csv(self.data_path, sep=',')

        # drop duplicate reviews
        self.data.drop_duplicates(subset=['Id'], inplace=True)

    def parse_document(self):

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

    def cleaning_reviews(self, remove_contractions=True, remove_special_characters=True,
                         remove_stopwords=False, lemmatise=True, tokenise=True):
        """
        This function preprocesses the reviews, carrying out multiple datapreprocessing steps including:

            1. Remove contractions (default=True) - Remove all contractions from the sentence
            2. Sentence is then tokenised for further preprocessing
            3. Remove special characters (default=True) - Remove special characters from tokens
            4. Remove stopwords (default=False) - The removal of stopwords is set to false based on the assumptions
               that stopwords do have an impact on the sentiment of the sentence.
            5. Lemmatise (default=True) - Lemmatise the words
            6. Tokenise (default=False) - Store end results as either tokens or sentences
        """
        ids = []

        for _, review_id in enumerate(self.ids):
            for sentence in self.dict_sentences[review_id]:
                # Remove contractions from characters
                if remove_contractions is True:
                    sentence = contractions.fix(sentence)

                # Tokenise sentence
                tokens = sentence.split(' ')

                # Remove special characters
                if remove_special_characters is True:
                    pattern = r'[^a-zA-z0-9\s]'
                    tokens = [re.sub(pattern, '', token) for token in tokens]

                # Remove stopwords
                if remove_stopwords is True:
                    tokens = [token.lower() for token in tokens if token.lower() not in self.stopwords]

                # Lemmatise text
                if lemmatise is True:
                    tokens = [self.lemmatizer.lemmatize(word) for word in tokens]

                if tokenise is False:
                    ids.append(review_id)
                    self.reviews.append(' '.join(tokens))
                else:
                    ids.append(review_id)
                    self.reviews.append(tokens)

        self.individual_sentences['review_id'] = ids
        self.individual_sentences['review'] = self.reviews

    def return_dataframe(self):
        self.reviews_cleaned = pd.DataFrame.from_dict(self.individual_sentences, orient='columns')
        relevant_info = self.data.loc[:, ['Id', 'Date']]
        self.reviews_cleaned = self.reviews_cleaned.merge(relevant_info, left_on='review_id',
                                                          right_on='Id', how='left')

        self.reviews_cleaned.drop(columns=['Id'], inplace=True)

    def do_all(self):
        self.read_data()
        self.parse_document()
        self.cleaning_reviews()


if __name__ == "__main__":
    data_prep = DataPrep()
    data_prep.read_data()
    data_prep.parse_document()
    data_prep.cleaning_reviews()
    data_prep.return_dataframe()
