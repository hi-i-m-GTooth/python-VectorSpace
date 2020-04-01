import nltk

def keepIt(word):
    t = nltk.pos_tag(word)[0][1]

    if t in ['NN','NNS','NNP','NNPS','VB','VBD','VBG','VBN','VBP','VBZ']:
        return True
    else:
        return False

