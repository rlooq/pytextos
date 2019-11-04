
import pickle

def add_stops(new):
    '''Takes a list of upper-case vocabulary items and adds it
       to master list of vocabulary stops'''
    with open("master_vocstops.pickle", "rb") as f:
        masterlist=pickle.load(f)
    newmaster=new+masterlist

    with open("master_vocstops.pickle", "wb") as f:
        pickle.dump(newmaster, f)
    
    print("{} new items were added to known vocabulary.".format(len(new)))


def filter_vocab_out(vocab):
    to_stops=[]
    to_use=[]
    for i in vocab:
        print(i)
        decision=input("\nAdd to known list? (y/n)")
        if decision=="y":
            to_stops.append(i)
        elif decision=="n":
            to_use.append(i)
        else:
            print("Wrong input. Start over.")
            break
    add_stops(to_stops)
    print("New vocabulary to use: {}.".format(str(to_use)))
