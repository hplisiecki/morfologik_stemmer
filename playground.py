# Import necessary libraries
# pyMorfologik is a Python wrapper for the Morfologik library (used for stemming and morphological analysis of words)
from pyMorfologik import Morfologik
from pyMorfologik.parsing import ListParser
import pickle  # used for loading/saving serialized Python objects
import requests  # allows sending HTTP requests to get data from the web

# Open and load a dictionary of lemmas (word stems) stored in a pickle file
with open('data/lemmatizer_dictionary.pickle', 'rb') as handle:
    lema_dict = pickle.load(handle)

# URL containing a list of Polish stopwords (common words like "and", "or", "the" that are often ignored in text processing)
dir = 'https://raw.githubusercontent.com/bieli/stopwords/master/polish.stopwords.txt'

# Download the stopwords file from the internet
r = requests.get(dir)

# Split the file content into a list where each line is a stopword
stopwords_list = r.text.splitlines()

# Initialize the parser and stemmer from Morfologik library
parser = ListParser()
stemmer = Morfologik()

# Import the 'string' library (used for string operations) - though it's not used here directly
import string

# Define a function called 'stem' that will process and stem (find base forms) of words in a sentence
# 'stopwords' argument controls whether stopwords should be removed or not
def stem(sentence, stopwords=False):
    # Remove punctuation marks from the sentence
    sentence = "".join([ch for ch in sentence if ch not in '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~'])

    # Split the sentence into individual words
    words = str(sentence).split(' ')

    # If 'stopwords' argument is True, filter out the stopwords from the list of words
    if stopwords:
        words = [word for word in words if word not in stopwords_list]

    # Join the remaining words back into a single string (without stopwords if filtered)
    tweet = ' '.join(words)

    # Use Morfologik stemmer to get base forms (lemmas) of the words
    morf = stemmer.stem([tweet.lower()], parser)

    # Initialize an empty string to store the processed sentence
    string = ''

    # Loop through each word's morphological analysis result
    for i in morf:
        # If the word is in the lemma dictionary, use its base form (lemma)
        if i[0] in lema_dict.keys():
            string += lema_dict[i[0]] + ' '
        else:
            # If it's not in the lemma dictionary, try to get the base form from Morfologik analysis
            try:
                string += list(i[1].keys())[0] + ' '
            # If Morfologik doesn't provide a base form, use the original word
            except:
                string += i[0] + ' '

    # Remove the trailing space at the end of the processed sentence
    string = string[:-1]

    # Return the final processed and stemmed sentence
    return string

# Example sentence in Polish that you want to process
sentence = 'Poszedłem do sklepu żeby kupić trochę mleka.'

# Print the stemmed version of the sentence
print(stem(sentence))
