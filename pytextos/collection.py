from pytextos.text import Text
import os, csv
from secrets import choice
import re

from tkinter import Tk, filedialog

# Helper function to select collection folder via dialog
def GetPath():
    root = Tk()
    root.withdraw()
    return filedialog.askdirectory()


# Collection class definition
class Collection:
    """Group of Text Objects to be collected, queried, listed, compared and
       exported according to different criteria: if no folder is provided in
       instance's parameters, it will be selected with a dialog.
    """

    def __init__(self, folder=None, title="Unnamed Collection"):
        
        self.title = title
        if folder:
            self.folder=folder
        else:
            self.folder = GetPath()
        # Validating folder
        try:
            os.chdir(self.folder)
            members= [Text(f) for f in os.listdir() if f.endswith(".txt")]
            members.sort(key=lambda f:f.token_count, reverse=True)
            self._members=members 
        except FileNotFoundError:
            print("Not a valid path.")
    
    def print_members(self):
        for text in self._members:
            print(f"{self._members.index(text)})".rjust(3), f"{text.title} - {text.by.split()[-1]}".ljust(76, "."), f"{text.token_count:,}".rjust(7), "words")

    def __repr__(self):
        return f"<Collection: {self.title}>"

    def __len__(self):
        return len(self._members)

    def __getitem__(self, i):
        return self._members[i]

    def to_csv(self, filename):
        with open(filename, "w", encoding="utf-8") as csvfile:
            collection_writer = csv.writer(
                csvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            headers = [
                "File",
                "Author",
                "Date",
                "Text_Type",
                "Genre",
                "Wordcount",
                "LexDiv",
                "Hapax_Richness",
                "Avg_Word_Len",
                "Avg_Sent_Len",
                "Read_Time",
                "Keywords",
            ]
            collection_writer.writerow(headers)
            for t in self._members:
                collection_writer.writerow(
                    [
                        t.filename,
                        t.by,
                        t.date,
                        t.text_type,
                        t.genre,
                        t.token_count,
                        t.lex_div_maas,
                        t.hapax_richness,
                        t.avg_word_len,
                        t.avg_sentence_len,
                        t.reading_time,
                        t.keywords,
                    ]
                )


    def random(self):
        random_text=choice(self._members)
        random_line=random_text.random_sent()
        if len(random_line)>8:
            return (f"{random_text.random_sent()}\n\t--{random_text.by}, {random_text.title}.\n")
        else:
            print("Try again.")

    def print_random(self):
        print(self.random())    