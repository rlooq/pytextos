import spacy
nlp=spacy.load('en_core_web_sm')

raw=open('boyle.txt', 'r', encoding='utf-8').read()

doc=nlp(raw)

print('This text has {} sentences.'.format(len(list(doc.sents))))
