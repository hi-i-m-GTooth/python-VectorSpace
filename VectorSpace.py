from pprint import pprint
from Parser import Parser
from tag import keepIt
import tfidf
import util
import sys
import os
import argparse

class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []
    #Collection of IDF
    IDFVector = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None

    # TF or TF-IDF
    way = ""


    def __init__(self, documents=[],way_=""):
        self.documentVectors=[]
        self.parser = Parser()
        self.way = way_
        if(len(documents)>0):
            self.build(documents,self.way)

    def build(self,documents,way):
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents)
        if way == "TF-IDF":
            self.IDFVector = self.getIDFVector(documents)
        self.documentVectors = [self.makeVector(document) for document in documents]
        
        #print(self.vectorKeywordIndex)
        #print(self.documentVectors)


    def getVectorKeywordIndex(self, documentList):
        """ create the keyword associated to the position of the elements within the document vectors """

        #Mapped documents into a single word string	
        vocabularyString = " ".join(documentList)

        vocabularyList = self.parser.tokenise(vocabularyString)
        #Remove common words which have no search value
        vocabularyList = self.parser.removeStopWords(vocabularyList)
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)


    def getIDFVector(self, documentList):
        vocabularyString = " ".join(documentList)
        wordList = self.parser.tokenise(vocabularyString)
        wordList = self.parser.removeStopWords(wordList)
        uniqWordList = util.removeDuplicates(wordList)
        IDFvector = [tfidf.idf(word,documents) for word in uniqWordList]
        return IDFvector
    
    
    def makeVector(self, wordString):
        """ @pre: unique(vectorIndex) """

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        if self.way == "TF-IDF":
            for i in range(0,len(vector)):
                vector[i] *= self.IDFVector[i]
        return vector


    def makeTagVector(self, wordString):

        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString)
        wordList = self.parser.removeStopWords(wordList)
        for word in wordList:
            if keepIt(word):
                vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        if self.way == "TF-IDF":
            for i in range(0,len(vector)):
                vector[i] *= self.IDFVector[i]*0.5
        return vector


    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings


    def search(self,searchList,way):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)

        if way == "cosine":
            ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        elif way == "euclid":
            ratings = [util.euclid(queryVector, documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings
    
    
    def f_search(self,searchList,doc,way):
        """ search for documents that match based on a list of terms """
        queryVector = self.buildQueryVector(searchList)
        fVector = self.makeTagVector(doc)

        for i in range(0,len(queryVector)):
            queryVector[i] += fVector[i]
        
        if way == "cosine":
            ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        elif way == "euclid":
            ratings = [util.euclid(queryVector, documentVector) for documentVector in self.documentVectors]
        #ratings.sort(reverse=True)
        return ratings
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="setting query")
    args = parser.parse_args()
    if args.query: # if query is empty then exit
        query = args.query.split(' ')
        print("Your Query is: "+str(query))

    documents = []
    doc_ids = []

    for file in os.listdir("doc"):
        with open(os.path.join("./doc",file)) as f:
            documents.append(f.read())
            doc_ids.append(file[:file.find('.')])

######################### Project 1 ############################
    
    vectorSpace = VectorSpace(documents)

    # Term Frequency (TF) Weighting + Cosine Similarity
    search_rlt = vectorSpace.search(query,"cosine")
    
    print("\n\nTerm Frequency (TF) Weighting + Cosine Similarity\n")
    print("%-7s %10s"%("DocID", "Score"))
    for i in range(0,5):
        index = search_rlt.index(max(search_rlt))
        max_value = search_rlt[index]
        print("%-7s %10f"%(doc_ids[index],round(max_value,6)))
        search_rlt[index]=-1

    # Term Frequency (TF) Weighting + Euclidean Distance
    search_rlt = vectorSpace.search(query,"euclid")
    
    print("\n\nTerm Frequency (TF) Weighting + Euclidean Distance\n")
    print("%-7s %10s"%("DocID", "Score"))
    for i in range(0,5):
        index = search_rlt.index(min(search_rlt))
        max_value = search_rlt[index]
        print("%-7s %10f"%(doc_ids[index],round(max_value,6)))
        search_rlt[index]=max(search_rlt)

   

    vectorSpace2 = VectorSpace(documents,"TF-IDF")
    feedback_index = -1
    # TF-IDF Weighting + Cosine Similarity
    search_rlt = vectorSpace2.search(query,"cosine")
    
    print("\n\nTF-IDF Weighting + Cosine Similarity\n")
    print("%-7s %10s"%("DocID", "Score"))
    for i in range(0,5):
        index = search_rlt.index(max(search_rlt))
        if i == 0: # feed back for Method 5
            feedback_index = index
        max_value = search_rlt[index]
        print("%-7s %10f"%(doc_ids[index],round(max_value,6)))
        search_rlt[index]=-1
    
    # TF-IDF Weighting + Euclidean Distance
    search_rlt = vectorSpace2.search(query,"euclid")
    
    print("\n\nTF-IDF Weighting + Euclidean Distance\n")
    print("%-7s %10s"%("DocID", "Score"))
    for i in range(0,5):
        index = search_rlt.index(min(search_rlt))
        max_value = search_rlt[index]
        print("%-7s %10f"%(doc_ids[index],round(max_value,6)))
        search_rlt[index]=max(search_rlt)


    # Feedback Queries + TF-IDF Weighting + Cosine Similarity
    search_rlt = vectorSpace2.f_search(query,documents[feedback_index],"cosine")
    
    print("\n\nFeedback Queries + TF-IDF Weighting + Cosine Similarity\n")
    print("%-7s %10s"%("DocID", "Score"))
    for i in range(0,5):
        index = search_rlt.index(max(search_rlt))
        if i == 0:
            feedback_index = index
        max_value = search_rlt[index]
        print("%-7s %10f"%(doc_ids[index],round(max_value,6)))
        search_rlt[index]=-1

###################################################
