# This file is the starting file for a rhyming program using NLTK.

import semidbm
import random
import time

from nltk.tokenize import RegexpTokenizer

# Open the rhyming database
syllablesDB = semidbm.open('words.db')
rhymesDB = semidbm.open('rhymes.db')


def rhyme(word, count):
    """Returns a list of all the words that rhyme with 'word' with 'count' number of syllables."""
    # start = time.time() #####
    try:
        wordSyllables = syllablesDB[word.upper()].decode().split()[0]
        # print wordSyllables ###
        wordRhymes = [word.decode() for word in rhymesDB[wordSyllables].split()]
        wordRhymes.remove(word.upper())
        # print wordRhymes ###
        backlist = [x.lower() for x in wordRhymes if count == 0 or syllablesDB[x].split()[1] == count]
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
        return int(syllablesDB[word.upper()].split()[1])
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
badwords = badstring.split()


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
        current_syllables = 0
        while current_syllables < length:
            possibilities = dictionary[(sentence[-2], sentence[-1])]
            sentence.append(possibilities[random.randrange(0, len(possibilities))])
            current_syllables += numSyllables(sentence[-1])
        # print sentence, currentSyllables

        if sentence[-1] not in badwords:
            if current_syllables == length and (target == '' or sentence[-1] in rhymes):
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
    #      EDIT HERE TO CHANGE THE POEM      #
    ##########################################
    rhyme_scheme = ['A', 'B', 'A', 'B']  # The rhyme scheme
    rhyme_definitions = {}  # Stores the rhyme sounds for each scheme
    poem_syllables = [8, 9, 10, 9]  # Number of syllables per line
    # syllablesPerLine = 10

    poem = ['i', 'say']
    # poem = ['the', 'mountain']
    poem_lines = [[poem[0], poem[1]]]
    for i in range(len(rhyme_scheme)):
        pattern = rhyme_scheme[i]
        target = ''
        if pattern in rhyme_definitions:
            target = rhyme_definitions[pattern]
        sentence = babble(poem_syllables[i], (poem[-2], poem[-1]), target, dictionary)
        # sentence = babble(syllablesPerLine, (poem[-2], poem[-1]), target, dictionary)
        if not sentence:
            return []
        if pattern not in rhyme_definitions:
            rhyme_definitions[pattern] = sentence[-1]
        # print sentence
        poem += sentence
        poem_lines.append(sentence)

        print(i)
    return poem_lines


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

# TODO: Questionable to remove words not in the rhymer; may revert this if it has adverse effects
syllables_keys = [s.decode() for s in syllablesDB.keys()]
full_corpus = [a.lower() for a in fileWords if a.upper() in syllables_keys]  # Convert all the tokens to lowercase

upTable, downTable = transitionTables(full_corpus)  # Generate trigram transition tables

# Generate poems until we have a valid one
print('...')
p = []
while not p:
    p = poem(full_corpus, upTable)
    print('...')  # Add some indication of progress

# Print the lines of the poem space-separated
fout = open('poems.txt', 'a')
fout.write('\n')
for line in p:
    print(' '.join(map(str, line)))
    fout.write('\n')
    fout.write(' '.join(map(str, line)))
