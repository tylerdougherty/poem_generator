# This file is the starting file for a rhyming program using NLTK.

import random
import string
import time

import dbm
from nltk.tokenize import RegexpTokenizer

# Open the rhyming database
syllablesDB = dbm.open('words.db')
rhymesDB = dbm.open('rhymes.db')


def rhyme(word, count):
    """Returns a list of all the words that rhyme with 'word' with 'count' number for syllables."""
    # start = time.time() #####
    try:
        wordSyllables = string.split(syllablesDB[string.upper(word)])[0]
        # print wordSyllables ###
        wordRhymes = string.split(rhymesDB[wordSyllables])
        wordRhymes.remove(string.upper(word))
        # print wordRhymes ###
        backlist = [string.lower(x) for x in wordRhymes if count == 0 or string.split(syllablesDB[x])[1] == count]
    except:
        backlist = []
    # print 'rhyme: '+str(time.time() - start) #####
    return backlist


def rhymesWith(word1, word2):
    """Determines if two words rhyme."""
    if word1.find(word2) == len(word1) - len(word2):
        return False
    if word2.find(word1) == len(word2) - len(word1):
        return False
    return word1 in rhyme(word2)


##### Only works with the NLTK library
# # Returns the number of sounds that match for the words
# def rhymeStrength(word1, word2):
# 	strength = 1
# 	while rhymesWith(word1, word2, strength):
# 		strength += 1
# 	return strength-1


def numSyllables(word):
    """Returns the number of syllables in 'word'."""
    try:
        return int(string.split(syllablesDB[string.upper(word)])[1])
    except:
        return 0


def transitionTables(words):
    """Creates trigram word transition tables from a token list."""
    upTable = {}
    downTable = {}
    size = len(words)
    for i in range(size):
        t1 = (words[i], words[(i + 1) % size])
        t2 = (words[i], words[i - 1])
        if t1 not in upTable:
            upTable[t1] = []
        if t2 not in downTable:
            downTable[t2] = []
        upTable[t1].append(words[(i + 2) % size])
        downTable[t2].append(words[i - 2])
    return upTable, downTable


# The words that should not end the line
badstring = '''to the for so and with of in but my it i a o oh can how
			at thou you no because your or she he'''
badwords = string.split(badstring)


def babble(length, seed, target, dictionary):
    """Returns a line with 'length' syllables, using 'seed' as the opening
		trigram but not including those words in the line, and where the
		last word of the line rhymes with 'target'; words are taken from
		'dictionary'. If 'target' is not specified, a random end word is
		selected."""
    st = time.time()  #####

    # Get all the words that rhyme with the target word, if we have one
    if target != '':
        rhymes = rhyme(target, 0)

        # If there are no words that rhyme with target, exit
        if len(rhymes) == 0:
            return []

    while True:
        sentence = [seed[0], seed[1]]
        currentSyllables = 0
        while currentSyllables < length:
            possibilities = dictionary[(sentence[-2], sentence[-1])]
            sentence.append(possibilities[random.randrange(0, len(possibilities))])
            currentSyllables += numSyllables(sentence[-1])
        # print sentence, currentSyllables

        if sentence[-1] not in badwords:
            if currentSyllables == length and (target == '' or sentence[-1] in rhymes):
                # for x in sentence:
                # 	print x, numSyllables(x)

                # print 'babble: '+str(time.time() - st) #####
                return sentence[2:]

        # Only look for matches for a specified amount of time
        if time.time() - st > 5:
            # print (time.time() - st) #####
            return []


def poem(corpus, dictionary):
    """Generates a poem."""

    ##########################################
    ###    EDIT HERE TO CHANGE THE POEM    ###
    ##########################################
    rhymeScheme = ['A', 'B', 'A', 'B']  # The rhyme scheme
    rhymeDefinitions = {}  # Stores the rhyme sounds for each scheme
    poemSyllables = [8, 9, 10, 9]  # Number of syllables per line
    # syllablesPerLine = 10

    poem = ['i', 'say']
    # poem = ['the', 'mountain']
    poemLines = [[poem[0], poem[1]]]
    for i in range(len(rhymeScheme)):
        pattern = rhymeScheme[i]
        target = ''
        if pattern in rhymeDefinitions:
            target = rhymeDefinitions[pattern]
        sentence = babble(poemSyllables[i], (poem[-2], poem[-1]), target, dictionary)
        # sentence = babble(syllablesPerLine, (poem[-2], poem[-1]), target, dictionary)
        if not sentence:
            return []
        if pattern not in rhymeDefinitions:
            rhymeDefinitions[pattern] = sentence[-1]
        # print sentence
        poem += sentence
        poemLines.append(sentence)

        print(i)
    return poemLines


# Not used in current implementation
# def randWord(count, corpus):
#     """Chooses a random word from 'corpus', with at least 'count' syllables."""
#     while True:
#         word = corpus[random.randrange(0, len(corpus))]
#         if word in cmud and len(cmud[word]) >= count and word != 'the':
#             return word


###################################################
# Start of the main program
###################################################
tokenizer = RegexpTokenizer(r'[A-Za-z\']+')  # Create a regex tokenizer
file = open('poemCorpus.txt').read()  # Open and read the file
fileWords = tokenizer.tokenize(file)  # Tokenize the file

#### Questionable to remove words not in the rhymer; may revert this if it has adverse effects
corpus = [string.lower(a) for a in fileWords if string.upper(a) in syllablesDB]  # Convert all the tokens to lowercase

upTable, downTable = transitionTables(corpus)  # Generate trigram transition tables

# Generate poems until we have a valid one
print('...')
p = []
while not p:
    p = poem(corpus, upTable)
    print('...')  # Add some indication of progress

# Print the lines of the poem space-separated
fout = open('poems.txt', 'a')
fout.write('\n')
for line in p:
    print(' '.join(map(str, line)))
    fout.write('\n')
    fout.write(' '.join(map(str, line)))
