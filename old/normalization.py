from contractions import CONTRACTION_MAP
import re
import nltk
import string
from nltk.stem import WordNetLemmatizer
import html
import unicodedata

stopword_list = nltk.corpus.stopwords.words('english')
wnl = WordNetLemmatizer()

# Function that tokenizes sentences
# Input -> review sentences
# Output -> tokens of review sentences
def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens

# Function that changes contracted words by its non-contracted form
# Input -> review sentences, contractions dictionary
# Output -> review sentences without contracted words
def expand_contractions(text, contraction_mapping):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

# Function that lematizes sentences
# Input -> review sentences
# Output -> lemmatized sentences
def lemmatize_text(text):
    lemmatized_tokens = [wnl.lemmatize(word)
                         for word in nltk.word_tokenize(text)]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text

# Function that removes special characters
# Input -> review sentences
# Output -> review sentences without special characters
def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

# Function that removes stopwords based on NLTK stopword dictionary
# Input -> review sentences
# Output -> review sentences without stopwords
def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

# Function that normalises the text
# Input -> review sentences
# Output -> review sentences without stopwords, contractions and special characters
# Lemmatization and tokenizing is not done here as it is done for specific parts of the code
def normalize_corpus(corpus, lemmatize=True, tokenize=False):
    normalized_corpus = []
    for text in corpus:
        text = html.unescape(text)
        text = expand_contractions(text, CONTRACTION_MAP)
        text = remove_special_characters(text)
        text = remove_stopwords(text)
        if lemmatize:
            text = lemmatize_text(text)
        else:
            text = text.lower()
        if tokenize:
            text = tokenize_text(text)
            normalized_corpus.append(text)
        else:
            normalized_corpus.append(text)

    return normalized_corpus

# Function that parses the reviews
# Input -> reviews
# Output -> review sentences 
def parse_document(document):
    document = re.sub('\n', ' ', document)
    if isinstance(document, str):
        document = document
    else:
        raise ValueError('Document is not string or unicode!')
    document = document.strip()
    sentences = nltk.sent_tokenize(document)
    sentences = [sentence.strip() for sentence in sentences]
    return sentences