# Social Media Analytics
This repository includes the code used for scrapping and analysing customer reviews for a specific company, in order to understand the sentiment associated with each review.

## Scrapping
Comments and reviews were scraped from Twitter, Reevoo.co.uk and Trustpilot.com for Currys website

## Analysis
The methodology followed a series of steps. Firstly, the reviews were normalised and divided into sentences. Then, bigrams and most common words were used to identify keywords in the comments. These keywords were used to develop a boolean rule to classify each sentence.

Finally, the sentiment of each sentence was analysed using Stanford and NLTK packages.
