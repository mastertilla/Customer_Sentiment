from pycorenlp import StanfordCoreNLP
import pandas as pd
import os
import datetime

import logging
logging.basicConfig(filename='sentiment_analyis.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalysis:
    def __init__(self, reviews=None, test=False):
        self.main_path = os.path.dirname(__file__)

        if reviews is None and test is False:
            self.reviews = pd.read_csv(os.path.join(self.main_path, "..", "results", "cleaned_reviews.csv"), sep=',')
            self.output_file = str(datetime.datetime.today().strftime('%Y-%m-%d')) + "_reviews_sentiment.csv"
        elif reviews is None and test is True:
            self.reviews = pd.read_csv(os.path.join(self.main_path, "..", "results", "cleaned_reviews_test.csv"), sep=',')
            self.output_file = str(datetime.datetime.today().strftime('%Y-%m-%d')) + "_reviews_sentiment_test.csv"
        else:
            self.reviews = reviews

        self.sentiment = []
    
    def initialise_stanford_nlpcore(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')
        self.operations = {'annotators': 'tokenize,lemma,pos,sentiment',
                           'outputFormat': 'json'}

    def gather_reviews(self):
        self.sentences = self.reviews['review_join'].tolist()

    def sentiment_reviews(self):
        for sentence in self.sentences:
            try:
                print('Sentence analysed: ' + sentence)
                results = self.nlp.annotate(sentence, self.operations)
                if isinstance(results, str):
                    logger.error("'CoreNLP request timed out. Your document may be too long'")
                    sentiment_i = 'Error'
                else:
                    sentiment_i = [result['sentiment'] for result in results['sentences']]
                print(sentiment_i)
            except TypeError:
                logger.error("Empty sentence found")
                continue

            self.sentiment.append(sentiment_i)

        self.reviews['sentiment'] = self.sentiment

    def save_results(self):
        save_file_path = os.path.join(self.main_path, "..", "results", self.output_file)
        self.reviews.to_csv(save_file_path, sep=',')

    def do_all_sentiment(self):
        self.initialise_stanford_nlpcore()
        self.gather_reviews()
        self.sentiment_reviews()
        self.save_results()


if __name__ == "__main__":
    sent = SentimentAnalysis(test=True)
    sent.do_all_sentiment()