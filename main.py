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

bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(finalList)
scored = finder.score_ngrams(bigram_measures.raw_freq) # ok. Stick with raw_freq, since likelihood_ratio returns
# different values for lip.

# scored = finder.score_ngrams(bigram_measures.likelihood_ratio)

# Group bigrams by first word in bigram.

suffix_sort = collections.defaultdict(list) # this contains information about the actual word and the frequencies.
# it's useful for the latter part, without imparting a new tuple onto the final dictionary.

suffix_keys = collections.defaultdict(list)

for key, scores in scored:
    suffix_keys[key[1]].append(key[0])

for key in suffix_sort:
    suffix_keys[key].sort(key = lambda x: -x[1])

# so now, we can presuppose input. You're given a letter (input1 == i1) AND the following word (input2 == i2).
# so, we use i2 to hash into the relevant list we want (i.e: find the relevant suffix)
# then, we continually go along the list, and return the FIRST word with the containing letter.
    # this is based on the heuristic that the MOST frequent collocation appears first, so we can simply utilize
    # this facet to return the word.

# what would the input take? two words? Let's assume that for now.
# this is the helper function that will be used for file I/O below...
def returnWord(startLetter, secondWord):
    prefixList = suffix_keys[secondWord]
    for prefix in prefixList:
        if (prefix[0] == startLetter):
            return prefix

# FILE I/O is below...
# kind of slapdash. Works though!

with open('input.txt', "r") as f1:
    with open('output.txt', "w") as f2:
        for line in f1:
            # now we can split...
            wordTuple = line.replace('\n', '').split(' ')
            # now to PROCESS the words...
            # wordTuple[0] is the letter
            # wordTuple[1] is the actual word

            guessWord = returnWord(wordTuple[0], wordTuple[1])
            f2.write("{} {}\n".format(guessWord, wordTuple[1]))

"""
blue ribbon
black hair
gray hair
green eye
red lip
beige box
white teeth
"""