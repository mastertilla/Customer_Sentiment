# Sentiment Analysis Tool
This tool scrappes, cleans and provides the sentiment of the sentences encountered in online reviews. In particular, the results presented are those of Curry's reviews on Truspilot. 

## Getting started

---

The next steps need to be done before being able to run the code.
First, clone this repo to your preferred location:

```
git clone git@github.com:mastertilla/Customer_Sentiment.git
```

### Pre-requisites

The Sentiment Analysis tool makes use of the NLPCore Algorithm developed at stanford. To make the algorithm work, it is necessary to run the coreNLP module first. The steps are as follows:

1. Ensure you have Java (1.8+) installed.
2. Download and unzip CoreNLP from https://stanfordnlp.github.io/CoreNLP/ in your preferred location
3. In the terminal, navigate to the CoreNLP folder.
4. Run ``java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 5000``

You also need to download Chromedriver (http://chromedriver.chromium.org/downloads) and save the .exe file into the repo folder.

### Installing

Dependendencies are installed through the pipenv files (go to you local directory where you clone the repo and run the following command):

```
pipenv install
```

## Running the code

If running from the terminal, you need to activate the pipenv environment from the terminal as:

```
pipenv shell
```

To generate the documentation, navigate to the docs folder, then run ``make html``. This will generate a folder with the html files containing the documentation. 

One these steps are done, the code is run from the terminal as main.py with the following options:

```
Usage:
  main.py [--scrape=<y/n>]
  main.py -h | --help
  main.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --scrape=<y/n>  Run scrapper (yes/no)
```

The results are stored in the results folder.
