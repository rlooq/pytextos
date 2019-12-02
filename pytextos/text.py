# Standard library imports to be used in methods
import string
from statistics import mean # to calculate avg word length
from collections import Counter
from . stopwords import ENGLISH_STOPS, KNOWN_VOCABULARY

# Definition of Text class

class Text:
    """ Text object. Collects text info, body in paragraphs, tokenizes and checks for keywords and vocabulary
        against a list of stopwords and known vocabulary"""

    def __init__(self, filename, text_type="Unspecified", genre="Unspecified"):
        """
        Initializes Text object by providing a .txt filename which is then parsed.
        `text_type` and `genre` are optional parameters which can be updated later.
        """
        self.filename = filename
        self.text_type = text_type
        self.genre = genre

        #Validating filename argument and raising exceptions.
        if filename.endswith(".txt"):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                self.title = lines[0].strip()
                self.by = lines[1].strip()
                self.date = lines[2].strip()
                self.subtitle = lines[3][1:-2] if lines[3].startswith("*") else None
                if self.subtitle == None:
                    self.body = [para for para in lines[3:-2] if para != "\n"]
                else:
                    self.body = [para for para in lines[4:-2] if para != "\n"]
                self.source = lines[-1]
            except FileNotFoundError:
                print("File not found in this directory.")
        else:
            print("Not a valid filename.")
            break #Not sure how this will work. Will the object be created anyway?

    def __repr__(self):
        return f'<Text \'{self.title}>'

    def __getitem__(self, i):
        return self.body[i]

    def __len__(self):
        return len(self.body)

    def tokenize(self):
        """
        Returns a list of word tokens from the body of the text
        """
        # Remove punctuation characters with string.maketrans()
        words = []
        for sent in self.body:
            words.extend(sent.strip().split())
        return [w.translate(str.maketrans("", "", string.punctuation)) for w in words if w.isalpha()]

    def word_count(self):
        return len(self.tokenize())

    def avg_word_len(self):
        return mean([len(w) for w in self.tokenize()])

    def lexical_diversity(self):
        return len(set(self.tokenize()))/len(self.tokenize())

    def freq_dist(self):
        """Returns a Counter object with word frequencies"""
        cnt = Counter()
        for word in self.tokenize():
            if word.lower() not in ENGLISH_STOPS:
                cnt[word.upper()] += 1
        return cnt

    def word_freq(self, word):
        """Returns number of occurrences of a given word, excluding stopwords"""
        freq=self.freq_dist()
        if word.upper() in freq:
            print(f'The word {word.upper()} appears {freq[word.upper()]} times in this text.')
        else:
            print(f'The word {word.upper()} is either a stopword or it\'s not used in this text.')

    # At the moment I have to idea how to tackle this one:
    def vocabulary(self):  # Need to refine this with a list of most common words or words by language level cefr?
        full=set([word.upper() for word in self.tokenize() if word.lower() not in ENGLISH_STOPS])
        return sorted([word.upper() for word in full if word not in (KNOWN_VOCABULARY) and word.isalpha()])