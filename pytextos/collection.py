from pytextos.text import Text
import os


class Collection:
    """Group of Text Objects to be collected, queried, listed, compared and
       exported according to different criteria.
    """
    def __init__(self, folder, title='Unnamed Collection'):
        self.folder=folder
        self.title=title
        # Validating folder
        try:
            os.chdir(folder)
            self.members=[Text(f) for f in os.listdir() if f.endswith('.txt')]
        except FileNotFoundError:
            print("Not a valid path.")

    def __len__(self):
        return len(self.members)    


    def __repr__(self):
        return f'<Collection: {self.title}>'
