import os
import sys
import random

# set random seed to system time
random.seed(None)


# creates a variation of a sequence
def variation(seq, key):
    # creates a set of random positions to change
    positions = []
    # converts string to a list in order to change the elements
    temp = list(seq)
    # creates L/10 random positions to change
    for i in range(int(round(len(temp) / 10))):
        positions.append(random.randint(0, len(temp)))
    # iterate over the random positions
    for j in positions:
        # creates a random number between 0 and 1
        prob = random.random()
        # changes a amino acid to another one chosen at random, checks to make sure
        # this is truly a new amino acid, tries again if not
        if prob <= 0.5:
            temp[j] = key.get(random.randint(0, 20))
            while temp[j] == seq[j]:
                temp[j] = key.get(random.randint(0, 20))
        # replaces one of the random positions with '-' to create a deletion.
        # Done this way because otherwise the check in the previous if statement
        # will no longer work properly after a deletion event
        else:
            temp[j] = '-'
    # converts the list to a string
    new_string = ''.join(temp)
    # strips off the '-' placeholders
    new_string = new_string.replace('-', '')
    return new_string


# I created this key from the BLOSUM62 matrix by just zipping the position of my matrix and the letter code
key = {0: 'A', 1: 'R', 2: 'N', 3: 'D', 4: 'C', 5: 'Q', 6: 'E', 7: 'G', 8: 'H', 9: 'I', 10: 'L', 11: 'K', 12: 'M',
         13: 'F', 14: 'P', 15: 'S', 16: 'T', 17: 'W', 18: 'Y', 19: 'V', 20: 'B', 21: 'Z', 22: 'X'}
f1 = open("C:/Users/Joshua/Google Drive/_grad school/Sp2018/cs466/Sequences/seq1.dat")

# prints sequences to separate files
s = [f1.read()]
for i in range(1, 6):
    file_name = "seq" + str(i) + ".dat"
    s.append(variation(s[i-1], key))
    print(s[i], file=open('C:/Users/Joshua/Google Drive/_grad school/Sp2018/cs466/Sequences/%s' % file_name, 'w'))

