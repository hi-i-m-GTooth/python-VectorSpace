# python-VectorSpace
implement Vector Space

## This project is based on Prof. Tsai (Victor Tsai)'s program.

## Before Starting
  #### Main Program
  * **VectorSpace.py:** the main part of creating VectorSpace and calculating results in **5 Methods**.
    * **Method 1:** Term Frequency (TF) Weighting + Cosine Similarity
    * **Method 2:** Term Frequency (TF) Weighting + Euclidean Distance
    * **Method 3:** TF-IDF Weighting + Cosine Similarity
    * **Method 4:** TF-IDF Weighting + Euclidean Distance
    * **Method 5:** Relevance Feedback *(Pseudo Feedback is the Nouns and the Verbs of the first document in **Method 3**)*
  #### Words Pre-processing
  * **Parser.py:** do "remove stopwords", "remove nasty words" and "break string into tokens and stem words".
  * **PorterStemmer.py:** stem the words.
  * **tag.py:** use NLTK for grammatical tagging.
  * **english.stop:** list of stopwords.
  #### Calculating
  * **tfidf.py:** calculate idf for words.
  #### Others
  * **util.py:** remove duplicate words from a list, calculate "cosine" and "euclid" similarity.

## Getting Started
Use *-q* or *--query* to input Query string. Note that **an empty string** is not allowed.
```bash
$ python VectorSpace.py --query "drill wood"
```

## Files Description
### VectorSpace.py
##### IN CLASS VECTORSPACE
 * *(New Attribute)* ```way_```: initalize Vector Space Object with attribute ```way_``` can change the type of weighting of Vector.
   * ```way_``` is **TF** weighting by default.
   * ```way_``` is **TF-IDF** weighting if it is ```"TF-IDF"```
 * *(New method)* ```getIDFVector```: firstly, combine all documents into a string then parse the string and remove duplicated words. Secondly, create a TF-IDF vector depends on those parsed and non-duplicated words with ```tfidf.idf```.
 * *(New method)* ```makeTagVector```: compared to method```makeVector```, this method uses ```tag.keepIt``` to filter words except Verbs or Nouns.
 * *(Modified method)* ```search```: I add a new parameter ```way```, which determines the type of related function.
   * Function will be **Cosine Similarity** if ```way``` is ```"cosine"```.
   * Function will be **Euclidean Distance** if ```way``` is ```"euclid"```.
 * *(New method)* ```f_search```: compared to method ```search```, this method is particularly made for implementing **Method 5: Relevance Feedback**. In this method, feedback query vector ```fVector``` is made of Nouns and the Verbs within the first document of the **Method 3**.
##### IN MAIN
 * Use ```argparse``` to parse input string as query.
 * Variable ```documents``` is a string list containing all documents in ```./doc```. 
 * Variable ```doc_ids``` is a string list all documents' ids.
 * Create 2 VectorSpace objects, ```vectorSpace``` and ```vectorSpace2```, for **TF based** and **TF-IDF based** methods respectively.
 * In 5 methods, 
   * if related function is **Cosine Similarity**, pick **5** documents **from large to small** according to scores.
   * if related function is **Euclidean Distance**, pick **5** documents **from small to large** according to scores.

### Parser.py
 * Nothing changed.
 
### PorterStemmer.py
 * Nothing changed.
 
### tag.py *(New file)*
 * Mainly supported by ```NLTK``` (Natural Language Toolkit).
 * *(New Function)* ```keepIt```: given a word, if it belongs to Verbs or Nouns then return ```True```. Else, return ```False```.

### english.stop
 * Nothing changed.

### tfidf.py *(New file)*
 * *(New Function)* ```n_contain(word, doclist)```: simple counter for number of documents including the given word.
 * *(New Function)* ```idf(word, doclist)```: simply retrun idf of the given word in doclist.
 ```python
 return math.log(len(doclist) / (1 + n_contain(word, doclist)))
 ```

### util.py *(Modified file)*
 * *(New Function)* ```cosine(vector1, vector2)```:
 ```python
 return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))
 ```
  * *(New Function)* ```euclid(vector1, vector2)```:
 ```python
 return norm(np.array(vector1)-np.array(vector2))
 ```

## Reference
 * NCCU Web Searching and Mining Courses in 2020
 * Argparse: https://docs.python.org/zh-tw/3/howto/argparse.html#introducing-optional-arguments
 * NLTK: https://www.nltk.org/
