import nltk
import re

def tokenize_text(sentences):
    tokenised_sentences = []

    print(sentences)
    tokens = [sentences.split(' ')]
    print(tokens)
    # contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), flags=re.IGNORECASE | re.DOTALL)
    #
    # expanded_text = contractions_pattern.sub(expand_match, sentence)
    # expanded_text = re.sub("'", "", expanded_text)
    # print(expanded_text)

    tokenised_sentences.append(tokens)

    return tokenised_sentences

def expand_contractions(sentences, contraction_mapping):
    for sentence in sentences:
        print(sentence)
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

        expanded_text = contractions_pattern.sub(expand_match, sentence)
        expanded_text = re.sub("'", "", expanded_text)
        print(expanded_text)

        return expanded_text
