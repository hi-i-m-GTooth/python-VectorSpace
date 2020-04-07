import math

def n_contain(word, doclist):
    counter = 0
    for doc in doclist:
        if word in doc:
            counter+1
    return counter

def idf(word, doclist):
    return math.log(len(doclist) / (1 + n_contain(word, doclist)))

########################################################33
