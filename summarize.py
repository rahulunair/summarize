"""text summarization based on nltk"""
from concurrent.futures import ProcessPoolExecutor as ppe
from dataclasses import dataclass
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.snowball import SnowballStemmer

@dataclass
class MetaWords:
    stemmer = SnowballStemmer("english")
    stopwords = stopwords.words("english")

def clean_words(word: str) -> str:
    """clean and stem word"""
    meta_words = MetaWords()
    ascii_only = lambda x: x in string.ascii_lowercase
    word = "".join(filter(ascii_only, word))
    if word in meta_words.stopwords:
        return None
    word = meta_words.stemmer.stem(word)
    return word

def word_freq(sentence: str) -> dict:
    """histogram of words in a sentence."""
    hist = {}
    words = word_tokenize(sentence)
    with ppe(max_workers=4) as exe:
        res = exe.map(clean_words, words)
    clean_list = list(filter(None, res))
    for word in clean_list:
        if word not in hist:
            hist[word] = 1
        else:
            hist[word] += 1
    return hist

def score_sentences(paragraph: str) -> dict:
    """score sentences in a paragraph."""
    hist = {}
    for sentence in paragraph:
        for word, freq in word_freq(sentence).items():
            if word in sentence:
                if sentence in hist:
                    hist[sentence] += freq
                else:
                    hist[sentence] = freq
    return hist

def summarize(texts):
    summary = []
    texts = sent_tokenize(texts)
    text_hist = score_sentences(texts)
    sum_vals = 0
    for text in text_hist:
        sum_vals += text_hist[text]
    avg = int(sum_vals / len(text_hist))
    for text in texts:
        if (text in text_hist) and (text_hist[text] >  0.9 * avg):
            summary.append(text)
    return " ".join(summary)


if __name__ == "__main__":
    texts = "This algorithm is especially useful if your \
            sNote that words MUST begin one level below the root, and cannot start in the middle of the graph.Say that your job is to write a filter \
            program which takes in a block of text and either accepts or rejects the block of text based on whether the text has expletives, \
            such as on Neopets."
    print(texts)
    
    print("="*90)
    print(summarize(texts))
    print("="*90)
