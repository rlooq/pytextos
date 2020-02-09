"""
Text objects created from text files, so certain information can be extracted
from them: title, tokens, word counts, number of paragraphs, reading time, frequency, etc.
To-dos: refine tokenization, streamline workflow (scraping->text object->formatting and exporting / persistence in db?)
Issues: tokenization not perfect, how to implement vocabulary, required formatting for scraped text files
"""

# Standard library imports to be used in methods
import string
from statistics import mean  # to calculate avg word length
from collections import Counter  # for frequency distributions
from math import sqrt, log
import re
from .stopwords import ENGLISH_STOPS, KNOWN_VOCABULARY


# Definition of Text class
class Text:
    """
    Text object. Collects text info, body in paragraphs, tokenizes and
    checks for keywords and vocabulary against a list of stopwords
    """

    def __init__(self, filename):
        """
        Initializes Text object by providing a .txt filename which is then parsed.
        `text_type` and `genre` are optional parameters which can be updated later.
        """
        self.filename = filename

        # Validating filename argument and raising exceptions.
        if filename.endswith(".txt"):
            try:
                with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                self.title = lines[0].strip()
                self.by = lines[1].strip()
                self.date = lines[2].strip()
                self.subtitle = lines[3][1:-2] if lines[3].startswith("*") else None
                self.body = [para for para in lines[3:-2] if para != "\n"]
                self.text_type = (
                    lines[-3][1:].strip() if lines[-3].startswith("+") else None
                )
                self.genre = (
                    lines[-2][1:].strip() if lines[-2].startswith("-") else None
                )
                self.source = lines[-1].strip()
            except FileNotFoundError:
                print("File not found in this directory.")
        else:
            print("The filename doesn't have a txt extension.")

    def __repr__(self):
        return f"<Text '{self.title} by {self.by} ({self.date})>"

    def __getitem__(self, i):
        return self.body[i]

    def __len__(self):
        return len(self.body)

    def tokenize(self):
        """
        Returns a list of word tokens from the body of the text
        """
        # Remove curly quotes with a maketrans() translation table
        words = []
        mapping = {
            '"': None,
            "\u201c": None,
            "\u201d": None,
            "\u2018": None,
            "\u2019": "'",
            "\u2012": " ",
            "\u2013": " ",
            "\u2014": " ",
            "\u2015": " ",
            "!": None,
            "?": None,
            "#": None,
            "$": None,
            "%": None,
            "&": None,
            "\\": None,
            "(": None,
            ")": None,
            "*": None,
            "+": None,
            ",": None,
            "-": " ",
            ".": None,
            "/": None,
            ":": None,
            ";": None,
            "<": None,
            "=": None,
            ">": None,
            "@": None,
            "[": None,
            "]": None,
            "~": None,
            "_": None,
            "`": None,
            "{": None,
            "}": None,
            "0": None,
            "1": None,
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,
            "7": None,
            "8": None,
            "9": None,
        }
        trans_table = str.maketrans(mapping)
        for sent in self.body:
            clean_sent = sent.translate(trans_table)
            words.extend(
                [w.strip("' ").upper() for w in clean_sent.split()]
            )  # remove single quotes but not apostrophe
        return words

    @property
    def token_count(self):
        return len(self.tokenize())

    @property
    def type_count(self):
        return len(set(self.tokenize()))

    @property
    def reading_time(self):
        """Returns reading time in rounded number of minutes (int) """
        return round(self.token_count / 265)

    @property
    def avg_word_len(self):
        return round(mean([len(w) for w in self.tokenize()]), 2)

    def lex_div(self, variant="maas"):
        """Takes type of lexical diversity measurement (ttr, summer, maas) and returns result.
        """
        if variant == "ttr":
            return round(self.type_count / self.token_count, 4)
        elif variant == "summer":
            return round(log(log(self.type_count)) / log(log(self.token_count)), 4)
        elif variant == "maas":
            return (log(self.token_count) - log(self.type_count)) / (
                log(self.token_count) ** 2
            )

    @property
    def lex_div_maas(self):
        return self.lex_div()

    @property
    def hapax_richness(self):
        freq = self.freq_dist()
        hapax = [w for w in freq if freq[w] == 1]
        return len(hapax) / self.token_count * 100

    @property
    def keywords(self):
        words = [i[0] for i in self.freq_dist().most_common(7)]
        return " ".join(words)

    def freq_dist(self):
        """Returns a Counter object with word frequencies"""
        cnt = Counter()
        for word in self.tokenize():
            if word.lower() not in ENGLISH_STOPS:
                cnt[word.upper()] += 1
        return cnt

    def word_freq(self, word):
        """Returns number of occurrences of a given word, excluding stopwords"""
        freq = self.freq_dist()
        if word.upper() in freq:
            print(
                f"The word {word.upper()} appears {freq[word.upper()]} times in this text."
            )
        else:
            print(
                f"The word {word.upper()} is either a stopword or it's not used in this text."
            )

    # At the moment I have to idea how to tackle this one:
    def vocabulary(
        self,
    ):  # Need to refine this with a list of most common words or words by language level cefr?
        full = set(
            [
                word.upper()
                for word in self.tokenize()
                if word.lower() not in ENGLISH_STOPS
            ]
        )
        return sorted(
            [
                word.upper()
                for word in full
                if word not in (KNOWN_VOCABULARY) and word.isalpha()
            ]
        )


# The problem of tokenizing: here's a dict of contractions in English for possible use
contractions = {
    "ain't": "not",
    "aren't": "not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he has is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how has is does",
    "I'd": "I had would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it has is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she has is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as is",
    "that'd": "that would had",
    "that'd've": "that would have",
    "that's": "that has is",
    "there'd": "there had would",
    "there'd've": "there would have",
    "there's": "there has is",
    "they'd": "they had would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what has is",
    "what've": "what have",
    "when's": "when has is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where has is",
    "where've": "where have",
    "who'll": "will",
    "who'll've": "who will have",
    "who's": "who has is",
    "who've": "who have",
    "why's": "why has is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have",
}
