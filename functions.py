import pandas as pd
import nltk
from pycorenlp import StanfordCoreNLP
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer



stemmer = nltk.stem.PorterStemmer()

# This function checks that all setences are strings and also removes text left when reviewers left no comments
# Input -> reviews dataset
# Output -> reviews dataset without duplicates or errors
def cleaning_dataset(dataset):
    counter = 0
    clean_dataset = pd.DataFrame()
    for i in range(0, len(dataset)):
        clean_review = pd.DataFrame()
        text = dataset['Review']
        tokens = text[i]
        empty_review = ['Reviewer left no comment']
        if type(tokens) != str or tokens in empty_review:
            counter = counter + 1
        else:
            try:
                review_number = dataset['Review_number'][i]
                day = dataset['day'][i]
                month = dataset['month'][i]
                year = dataset['year'][i]
                clean_review = pd.DataFrame({'Review': tokens, 'Review_number': review_number,
                                             'day': day, 'month': month,
                                             'year': year}, index=[0])
            except KeyError:
                day = dataset['day'][i]
                month = dataset['month'][i]
                year = dataset['year'][i]
                clean_review = pd.DataFrame({'Review': tokens,
                                             'day':day, 'month':month,
                                             'year': year}, index=[0])

        clean_dataset = pd.concat([clean_dataset, clean_review])


    print("Number of reviews deleted from dataset: " + str(counter))
    clean_dataset = clean_dataset.reset_index(drop=True)
    return clean_dataset

# Function to create a list of sentences, instead of a dataset
# This is done to run the bigrams and most common words functions
# Input -> review sentences dataset
# Output -> a list with all sentences
def create_text(data):
    text = []
    for i in range(0, len(data)):
        sentence = data.iloc[i]
        text.append(sentence)
    return text


# This function returns the 30 most common bigrams and the 30 most common words
# Input -> list with all sentences
# Output -> list with 30 most common bigrams (and txt file) & 30 most common words (and txt file)
def most_freq_bigrams(text, datainput):
    bi_txt = open(str(datainput) + "_bigrams.txt", "w+")
    com_word = open(str(datainput) + "_comm_word.txt", "w+")

    bigram_text = []
    for i in range(0, len(text)):
        tokens = nltk.word_tokenize(text[i])
        for token in tokens:
            bigram_text.append(token)

    bigrams = nltk.bigrams(bigram_text)

    # Most frequent bigrams
    freq_bigrams = nltk.FreqDist(bigrams)
    most_common_bigrams = freq_bigrams.most_common(30)
    for most_common_bigram in most_common_bigrams:
        print(most_common_bigram)
        line = 'Bigram;'
        for x in most_common_bigram:
            if isinstance(x, int):
                line = line + str(x)
            else:
                for i in x:
                    line = line + i
                    line = line + ';'
        bi_txt.write(line + '\n')

    bi_txt.close()

    # Most frequent words
    freq_words = nltk.FreqDist(w.lower() for w in bigram_text)
    freq_words_30 = freq_words.most_common(30)

    # ten most frequent words
    print(freq_words_30)

    for freq_word in freq_words_30:
        line = 'FreqWord;'
        for x in freq_word:
            if isinstance(x, int):
                line = line + str(x)
            else:
                line = line + x + ';'
        com_word.write(line + '\n')
    com_word.close()

    return [most_common_bigrams, freq_words_30]

# Function that tags sentences based on lists of common issues
# Input -> review sentences dataset & list of stemmed key terms 
# Output -> review sentences dataset with an extra column per key term list (and 1 if the term is found in the sentence)
def tagging_reviews(data, del_list, cust_list):
    tags = pd.DataFrame()
    for i in range(0, len(data)):
        tags_i = pd.DataFrame()
        sentence = data[i]
        del_tag = 0
        cust_tag = 0
        oth_tag = 0
        for word in nltk.word_tokenize(sentence):
            stemmed_token = stemmer.stem(word)
            if stemmed_token in del_list:
                del_tag = del_tag + 1
            elif stemmed_token in cust_list:
                cust_tag = cust_tag + 1
            else:
                oth_tag = oth_tag + 1

        delivery_tag = 0
        customer_tag = 0
        other_tag = 0
        if del_tag >= 1:
            delivery_tag = 1
            if cust_tag >= 1:
                customer_tag = 1
        elif cust_tag >= 1:
            customer_tag = 1
        elif oth_tag >= 1:
            other_tag = 1

        tags_i = pd.DataFrame({'Delivery?': delivery_tag, 'Customer_service?': customer_tag, 'Other?': other_tag}, index=[0])
        tags = pd.concat([tags, tags_i])
    tags = tags.reset_index(drop=True)
    print("Number of reviews evaluated " + str(i + 1))

    return tags

# Function that returns the sentiment of a sentence based on Stanford Methodology
# Input -> review sentences dataset
# Output -> review sentences dataset with an extra column including the sentiment of the sentence
def sentiment_analysis_Stanford(data):
    nlp = StanfordCoreNLP('http://localhost:9000')

    operations = {'annotators': 'tokenize,lemma,pos,sentiment',
                  'outputFormat': 'json'}

    text = data['Review']
    errors = 0

    sent_data = pd.DataFrame()

    sent_neg = 0
    sent_pos = 0
    sent_neut = 0
    for i in range(0, len(text)):
        sentence = text[i]
        results = nlp.annotate(sentence, operations)
        sent_i = pd.DataFrame()
        try:
            for res in results["sentences"]:
                sentiment = res["sentiment"]
                if sentiment == "Negative":
                    sent = "negative"
                    sent_neg = sent_neg + 1
                elif sentiment == "Positive":
                    sent = "positive"
                    sent_pos = sent_pos + 1
                else:
                    sent = "neutral"
                    sent_neut = sent_neut + 1
            sent_i = pd.DataFrame({"Sentiment": sent}, index=[0])
            sent_data = pd.concat([sent_data, sent_i])
        except TypeError:
            sent = 'error'
            sent_i = pd.DataFrame({"Sentiment": sent}, index=[0])
            sent_data = pd.concat([sent_data, sent_i])
            errors = errors + 1
        print("Review: " + str(i))
    print('There were ' + str(errors) + ' errors when analysing sentiments')

    sent_data = sent_data.reset_index(drop=True)

    print('There are ' + str(sent_neg) + ' negative reviews, ' + str(sent_pos) + ' positive reviews and ' + str(sent_neut) + ' neutral reviews based on Stanford methodology')

    return sent_data


# Function that returns the sentiment of a sentence based on NLTK Methodology
# Input -> review sentences dataset
# Output -> review sentences dataset with an extra column including the sentiment of the sentence
def sentiment_analysis_SentiWord(dataset_tagged):
    text = dataset_tagged['Review']
    wn_lem = WordNetLemmatizer()

    sent_pos = 0
    sent_neg = 0
    sent_neut = 0

    sent_data = pd.DataFrame()

    for i in range(0, len(text)):
        sentence = text[i]
        pos_i = 0
        neg_i = 0

        for token in nltk.word_tokenize(sentence):
            lemma = wn_lem.lemmatize(token)
            if len(wn.synsets(lemma))>0:
                synset = wn.synsets(lemma)[0]
                sent = swn.senti_synset(synset.name())
                pos_i = pos_i + sent.pos_score()
                neg_i = neg_i + sent.neg_score()

        print("Sentence: " + str(i) + "Positive sentiment: " + str(pos_i) + "negative sentiment: " + str(neg_i))

        if pos_i < neg_i:
            sent = "negative"
            sent_neg = sent_neg + 1
        elif pos_i > neg_i:
            sent = "positive"
            sent_pos = sent_pos + 1
        else:
            sent = "neutral"
            sent_neut = sent_neut + 1
        sent_i = pd.DataFrame({"Sentiment": sent}, index=[0])
        sent_data = pd.concat([sent_data, sent_i])
        
        print("Review: " + str(i))

    sent_data = sent_data.reset_index(drop=True)

    print('There are ' + str(sent_neg) + ' negative reviews, ' + str(sent_pos) + ' positive reviews and ' + str(
        sent_neut) + ' neutral reviews based on SentiWordNet methodology')

    return sent_data




