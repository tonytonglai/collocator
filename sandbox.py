import nltk
from nltk.stem import WordNetLemmatizer
from nltk.collocations import *
nltk.download('omw-1.4')
# nltk.download('brown')
from nltk.corpus import brown
lemmatizer = WordNetLemmatizer()
import collections

# https://www.nltk.org/api/nltk.collocations.html
# use this for collocation afterwards? NLTK GOATed

# so maybe workflow is to tokenize, and then lemmatize? Wonder if that dramatically shifts anything
# will probably need multiple lists to store the intermediary data... or... wait. no.
# can just tokenize AND lemmatize in the same loop regarding the same word.

# edge case! Lemmatizer WON'T lemmatize words that are capitalized. I guess it thinks it's a proper noun? Two workarounds:
    # 1. simply remove the capitalized words (risks impacting some words)
    # 2. keep... but do the capitalized words == uncapitalized for all intents and purposes?

# way to access terms in the brown corpus
# print(brown.words()[:40])
finalList = list()

for word in brown.words():

    if word.isalpha(): # prunes the white space. but, do I want to do that? It is rather unnecessary
        # it helps delimit words and prevent weird associations where there isn't any.
        # i can move .isalpha() to later on in the processing when i try to do colocation
        tempWord = lemmatizer.lemmatize(word)
        finalList.append(tempWord)
#
# text = nltk.Text(finalList)
# text.collocations(num=20)
# print(finalList[:100])
# print(brown.words()[:100])

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(finalList)
# print("FINDER NBEST:")
# print(finder.nbest(bigram_measures.pmi, 10))
# print("\n\n")
scored = finder.score_ngrams(bigram_measures.likelihood_ratio)

# Group bigrams by first word in bigram.
prefix_keys = collections.defaultdict(list)
suffix_keys = collections.defaultdict(list)

for key, scores in scored:
    suffix_keys[key[1]].append(key[0])

for key in prefix_keys:
    suffix_keys[key].sort(key = lambda x: -x[1])

print("hair", suffix_keys["hair"][:10]) # NICE. You've captured all the relevant data...


for key, scores in scored: # TODO: swap to suffix key AFTER.
   prefix_keys[key[0]].append((key[1], scores)) # TODO: switch key[0] to key[1] and vice versa

# Sort keyed bigrams by strongest association.
for key in prefix_keys:
   prefix_keys[key].sort(key = lambda x: -x[1])

print("United", prefix_keys["United"][:10])
# **************************** SAMPLE GROUND BELOW ***************************************************************
# print("SCORED ARR")
# print(scored[:10])
# print(scored[0])
# print(scored[0][1])
# print("\n")
# newScored = sorted(scored, key= lambda bigTuple: bigTuple[0][1], reverse=True ) # returns a new list. does it modify the old one? probably not.
# # newScored = scored
# finalScored = [bigram[0] for bigram in newScored]
# print(finalScored[:10])
# # print(newScored[:10])
# # print(newScored[0])
# # print(newScored[0][1])
# # print("\n")
# print("\n\n")
#
# newDict = {} # used to store the variables...
# # dictionary will update the key based on what comes LAST. since we sorted the final array based on ASCENDING frequency
# # the assumption is that only the LAST element will be the relevant one, and it will be okay to overwrite.
#
# # recall that ultimately, we want to submit a pair of words; only the SECOND word will register becasue the first one will be absent.
# # but, how will this work in the absence of the letter?
#
# # should it be a list? Prevents collision so multiple words (of different starting letters) can be stored accordingly
# for bigram in finalScored:
#     newDict[bigram[1]] = bigram[0]
#
# print(newDict["States"])

# newArr = sorted(bigram for bigram, score in scored)
# print("SORTED ARR")
# print(newArr[:10])
# print("\n")
newDict = {} # we'll store all associations here. ASSUMING stored returns things in sorted order of frequency...
# it seems like it sorts based on alphabetical order though...?
# for

# newArr = sorted(finder.nbest(bigram_measures.raw_freq(), len(finder)))
# print(newArr)

# for tuple in finder:
#     print(tuple[0], tuple[1]) # since it's stored in [(x, y), ...] format.

# newArr = list(finder.nbest(bigram_measures.pmi, 100))
# print(newArr)
# print('yeah: ', newArr[0])
# print(finder)