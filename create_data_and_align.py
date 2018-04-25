import os
import sys
import random
#set random seed to system time
random.seed(None)


# converts numbers to string for randomized selection
def num_to_string(num):
    if num == 1:
        return 'A'
    elif num == 2:
        return 'C'
    elif num == 3:
        return 'T'
    elif num == 4:
        return 'G'
    else:
        raise Exception


# creates a random nucleotide string of length "length"
def rand(length):
    string = ''
    for i in range(length):
        string += num_to_string(random.randint(1, 4))
    return string


# creates a variation of a sequence
def variation(seq):
# creates a set of random positions to change
    positions = []
# converts string to a list in order to change the elements
    temp = list(seq)
# creates L/10 random positions to change
    for i in range(int(round(len(temp)/10))):
        positions.append(random.randint(0, len(temp)-1))
# iterate over the random positions
    for j in positions:
# creates a random number between 0 and 1
        prob = random.random()
# changes a nucleotide to another one chosen at random, checks to make sure
# this is truly a new nucleotide, tries again if not
        if prob <= 0.5:
            temp[j] = num_to_string(random.randint(1, 4))
            while temp[j] == seq[j]:
                temp[j] = num_to_string(random.randint(1, 4))
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

# takes a system argument as the length
L = int(sys.argv[1])
s1 = rand(L)
s2 = variation(s1)
s3 = variation(s1)

#prints sequences to separate files
print('>seq1\n' + s2, file=open('data/seq1.txt', 'w'))
print('>seq2\n' + s3, file=open('data/seq2.txt', 'w'))

# calls the DynamicProgramming.py program and outputs results to a text file.
os.system('DynamicProgramming.py data/seq1.txt data/seq2.txt data/array.txt -500 > result.txt')

