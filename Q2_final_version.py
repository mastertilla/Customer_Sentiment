import pandas as pd

import functions as fn
import normalization as nm

# Files with reviews to read 
files = ['Trustpilot_reviews.csv', 'Reevoo_reviews.csv']

# Run code for each of the files
for i in files:

    print("\n###### GATHERING DATASETS ######\n")

    # This defines the name of the output files
    if i == 'Reevoo_reviews.csv':
        datainput = 'Reevoo'
        print("The dataset used includes reviews from www.reevoo.co.uk\n")
    else:
        datainput = 'TP'
        print("The dataset used includes reviews from www.trustpilot.com\n")



    # Reads CSV file
    print("\n### Creating dataset ###\n")
    # First we load the dataset and keep only the first 1000 reviews
    dataset_original = pd.read_csv(i, sep=';',
                                   names=['Index', 'Review', 'day', 'month', 'year'])

    print("Number of reviews in original dataset: " + str(len(dataset_original)))


    print("\n###### TEXT NORMALIZATION ######\n")
    print("\n### Deleting unuseful reviews ###\n")

    # Removing duplicates
    dataset = fn.cleaning_dataset(dataset_original)


    print("\n### Normalizing reviews ###\n")

    # Normalising text
    normalised_text_dataframe = pd.DataFrame()

    # Run for each review and collect sentence, day, month and year
    for i in range(0, len(dataset)):
        text = dataset['Review'][i]
        day = dataset['day'][i]
        month = dataset['month'][i]
        year = dataset['year'][i]

        norm_text_data = pd.DataFrame()
        sentences = nm.parse_document(text)
        normalised_sentences = nm.normalize_corpus(sentences)

        normalised_text_data = pd.DataFrame()
        for j in range(0, len(normalised_sentences)):
            normalised_text = normalised_sentences[j]
            norm_text_data_j = pd.DataFrame({'Review_number': i,'Review': normalised_text, 'day': day, 'month': month,
                                           'year': year}, index=[0])
            norm_text_data = pd.concat([norm_text_data, norm_text_data_j])

        normalised_text_dataframe = pd.concat([normalised_text_dataframe, norm_text_data])
        normalised_text_dataframe = normalised_text_dataframe.reset_index(drop=True)

    print("Number of normalized reviews: " + str(i+1))

    print("\n### Gathering the reviews ###\n")

    # Create list of sentences for analysis of bigrams and most common words
    text = normalised_text_dataframe['Review']
    full_text = fn.create_text(text)

    # The next step is to calculate bigrams and most frequent words
    print("\n### Most frequent bigrams and words ###\n")
    most_common_bigrams, most_common_words = fn.most_freq_bigrams(full_text, datainput)



    print("\n###### TEXT MINING ######\n")

    # Create list of main key issues to be tagged
    # Variants of delivery (noun) and deliver (verb) when stemmized
    delivery_list = ['deliver', 'deliveri']
    customer_service_list = ['custom', 'servic'] # Including customer because it could mean customer service even if used in different context

    dataset_for_mining = normalised_text_dataframe['Review']


    print("\n### Tagging reviews as related to delivery, customer service or others ###\n")

    # Run function to tag sentences and add to the existing review sentences dataset
    reviews_tags = fn.tagging_reviews(dataset_for_mining, delivery_list, customer_service_list)
    dataset_tagged = pd.concat([normalised_text_dataframe, reviews_tags], axis=1)


    print("\n###### SENTIMENT ANALYSIS ######\n")

    # Run sentiment analysis methodologies (Stanford and NLTK) and add sentiment column to dataset
    # Finally, export final result to csv
    res_stanford = fn.sentiment_analysis_Stanford(dataset_tagged)
    res_sentiWord = fn.sentiment_analysis_SentiWord(dataset_tagged)
    final_dataset = pd.concat([dataset_tagged, res_stanford, res_sentiWord], axis=1)

    final_dataset.columns = ['Review_text', 'Review_number', 'day', 'month', 'year', 'Customer_service?',
                             'Delivery?', 'Other?', 'Sentiment_Stanford', 'Sentiment_SentiWord']

    final_dataset.to_csv(str(datainput)+'_reviews_analysed.csv', sep=';', mode='a',
                         header=True)
