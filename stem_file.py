# Import necessary libraries
from pyMorfologik import Morfologik  # Used for morphological analysis and stemming
from pyMorfologik.parsing import ListParser  # Used for parsing input for the Morfologik stemmer
import pickle  # Used for loading serialized Python objects
import requests  # Used for downloading data from the web
import multiprocessing  # Used for parallel processing
import pandas as pd  # A library used for working with data structures like DataFrames

# Open and load a pre-saved lemma dictionary from a pickle file
with open('D:\\GitHub\\morfologik_stemmer\\data\\lemmatizer_dictionary.pickle', 'rb') as handle:
    lema_dict = pickle.load(handle)

# URL containing a list of Polish stopwords (words to be ignored in text processing)
dir = 'https://raw.githubusercontent.com/bieli/stopwords/master/polish.stopwords.txt'

# Download the stopwords list from the URL
r = requests.get(dir)

# Split the downloaded content into a list where each line is a stopword
stopwords_list = r.text.splitlines()

# Initialize the Morfologik parser and stemmer
parser = ListParser()
stemmer = Morfologik()


# Define a function that will stem (get base forms) words from a sentence
def stem(sentence, stopwords=False):
    # Remove punctuation from the sentence
    sentence = "".join([ch for ch in sentence if ch not in '!"#$%&\'()*+,-./:;<=>?[\\]^_`{|}~'])

    # Split the sentence into words
    words = str(sentence).split(' ')

    # If stopwords removal is enabled, filter out stopwords from the list of words
    if stopwords:
        words = [word for word in words if word not in stopwords_list]

    # Join the words back into a single string for processing
    tweet = ' '.join(words)

    # Stem the words using the Morfologik stemmer
    morf = stemmer.stem([tweet.lower()], parser)

    # Initialize an empty string to store the final processed sentence
    string = ''

    # Loop through the stemmed words and process them
    for i in morf:
        # If the word is in the lemma dictionary, replace it with the base form
        if i[0] in lema_dict.keys():
            string += lema_dict[i[0]] + ' '
        else:
            # If not in the dictionary, try to get the base form from the Morfologik analysis
            try:
                string += list(i[1].keys())[0] + ' '
            # If Morfologik doesn't provide a base form, keep the original word
            except:
                string += i[0] + ' '

    # Remove the trailing space at the end of the sentence
    string = string[:-1]

    # Return the final processed and stemmed sentence
    return string


# The main part of the program (only runs when the script is executed directly)
if __name__ == '__main__':
    # Load a CSV file into a pandas DataFrame. This file contains the sentences to be processed.
    df = pd.read_csv(r'D:\\GitHub\\morfologik_stemmer\\data\\test_df.csv')

    # Extract the 'sentence' column and convert each sentence to a string (in case some are not)
    texts = [str(text) for text in df['sentence']]
    print(len(texts))  # Print the total number of sentences
    print('loaded Tweets')

    # Remove duplicate sentences to reduce redundant processing
    texts_set = list(set(texts))
    print(len(texts_set))  # Print the number of unique sentences

    # Create a multiprocessing pool with 16 workers for parallel processing
    pool = multiprocessing.Pool(16)

    # Stem all unique sentences using the stem() function and multiprocessing to speed up processing
    L = [pool.map(stem, texts_set)]
    print('stemmed')  # Notify that stemming is done

    # Create a dictionary that maps the original unique sentences to their stemmed versions
    dictionary = dict(zip(texts_set, [line for line in L[0]]))
    print('dictionary created')  # Notify that the dictionary is created

    # Replace each sentence in the original list with its stemmed version using the dictionary
    texts = [dictionary[line] for line in texts]

    # Close the multiprocessing pool to free resources
    pool.close()
    del pool  # Delete the pool object

    # Add a new column 'stemmed_sentence' to the DataFrame with the stemmed sentences
    df['stemmed_sentence'] = texts

    # Save the DataFrame back to the CSV file, overwriting the old data
    print("Saving...")
    df.to_csv(r'D:\\GitHub\\morfologik_stemmer\\data\\test_df.csv', index=False)
    print("Stemming finished.")  # Notify that the process is complete
