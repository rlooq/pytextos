import pytextos as pt

def test():
    doc=pt.Text('boyle.txt')
    print('-------------------------------------------------------------------')
    print(f'Text {doc.title} successfuly created.')
    print(f'Author: {doc.by}.')
    print(f'Date: {doc.date}.')
    print(f'It has {len(doc)} paragraphs and {doc.word_count()} words.')
    print(f'It would take aproximately {doc.reading_time()} minutes to read it.')
    print(f'Lexical diversity: {doc.lexical_diversity()}')
    print(f'Average word length: {doc.avg_word_len()} letters')
    print('-------------------------------------------------------------------')
    print('20 most common words:')
    for w in doc.freq_dist().most_common(20):
        print(w[0], end=", ")
    print('\n\n******')
    print('\nVocabulary:')
    for w in doc.vocabulary():
        print(w, end=', ')
    print('\n-------------------------------------------------------------------')

if __name__ == "__main__":
    test()
    
