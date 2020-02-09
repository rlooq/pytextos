from pytextos.text import Text
import os, csv


class Collection:
    """Group of Text Objects to be collected, queried, listed, compared and
       exported according to different criteria.
    """

    def __init__(self, folder, title="Unnamed Collection"):
        self.folder = folder
        self.title = title
        # Validating folder
        try:
            os.chdir(folder)
            self._members = [Text(f) for f in os.listdir() if f.endswith(".txt")]
        except FileNotFoundError:
            print("Not a valid path.")

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
                "Title",
                "Author",
                "Date",
                "Text_Type",
                "Genre",
                "Wordcount",
                "LexDiv",
                "Hapax_Richness",
                "Avg_Word_Len",
                "Read_Time",
                "Keywords",
            ]
            collection_writer.writerow(headers)
            for t in self._members:
                collection_writer.writerow(
                    [
                        t.title,
                        t.by,
                        t.date,
                        t.text_type,
                        t.genre,
                        t.token_count,
                        t.lex_div_maas,
                        t.hapax_richness,
                        t.avg_word_len,
                        t.reading_time,
                        t.keywords,
                    ]
                )
