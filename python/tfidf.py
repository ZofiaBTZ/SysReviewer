import re
import math
from nltk.corpus import wordnet as wn
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

with open("./stopwords_long.txt") as f:
    stop_words = [word for line in f for word in line.split()]
#print stop_words

    
def get_word_frequencies(text):
    raw_words = separate_words(text)
    total_word_count = len(raw_words)
    word_frequencies = {}

    for word in raw_words:
        if not word in word_frequencies:
            word_frequencies[word] = {"count": 1, "frequency": (1+0.001)/total_word_count}
        else:
            word_frequencies[word]["count"] += 1
            word_frequencies[word]["frequency"] = (word_frequencies[word]["count"]+0.0001)/total_word_count

    return word_frequencies

def separate_words(text, min_word_return_size=2):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        # leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and \
           current_word != '' and \
           not is_number(current_word) and \
           not current_word in stop_words and \
           current_word in nouns:
            words.append(current_word)
    return words

def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False

def calculate(df, total_doc_count, docs_with_word):
    #print(total_doc_count)
    #print(docs_with_word)
    return(df * math.log(total_doc_count / (1.00 + docs_with_word)))
