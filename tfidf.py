import math

def n_contain(word, doclist):
    counter = 0
    for doc in doclist:
        if word in doc:
            counter+1
    return counter

def idf(word, doclist):
    #bloblist = [tb(doc) for doc in doclist]
    return math.log(len(doclist) / (1 + n_contain(word, doclist)))

#def tfidf(word, blob, doclist):
    #return tf(word, blob) * idf(word, bloblist)

########################################################33
