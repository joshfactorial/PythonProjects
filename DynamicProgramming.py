# Joshua Allen
# 676067230
# Assignment 3
# 

import numpy as np
import sys


# read in file, stripping off the fasta code and 
# joining the separate lines into one, then
# making it all upper case for consistency
def read_seq(file) -> str:
    with open(file) as file:
        seq = file.readline().rstrip('\n')
        for line in file:
            if seq[0] == '>':
                seq = line.rstrip('\n').upper()
            else:
                seq += line.rstrip('\n').upper()
    return seq


# Read in the scoring matrix, stripping off the characters
def read_matrix(file):
    f = open(file)
    AAs = f.readline().strip().strip('\n').split("  ") # reads the first line to get the sequence catalog
    for line in f:
        matrix = []
        line = line.strip('\n')
        line = line.strip(' ')
        matrix.append(list(map(int, line.split()[1:])))
    key = dict(zip(AAs, list(np.arange(len(AAs)))))
    return matrix, key

# set variables to inputted arguments
seq1 = read_seq(sys.argv[1])
seq2 = read_seq(sys.argv[2])
blosum = read_matrix(sys.argv[3])
gap_score = int(sys.argv[4])

m = len(seq1)
n = len(seq2)

# initialize scoring matrix
D = np.zeros((m + 1, n + 1), dtype=int)

# scores at the edges
for i in range(1, m+1):
    D[i, 0] = D[i - 1, 0] + gap_score

for j in range(1, n+1):
    D[0, j] = D[0, j - 1] + gap_score

# Dynamic programming algorithm
for i in range(1, m + 1):
    for j in range(1, n + 1):
        match = D[i - 1, j - 1] + sim_mat[string_to_num(seq1[i - 1]),
                                          string_to_num(seq2[j - 1])]
        D[i, j] = max(D[i, j - 1] + gap_score, D[i - 1, j] + gap_score,
                      match)

i = m
j = n
seq1_aln = ''
seq2_aln = ''
score = 0

# reverse trace
while i > 0 and j > 0:
    if D[i, j] - sim_mat[string_to_num(seq1[i - 1]),
                         string_to_num(seq2[j - 1])] == D[i - 1, j - 1]:
        seq1_aln = seq1[i - 1] + seq1_aln
        seq2_aln = seq2[j - 1] + seq2_aln
        i = i - 1
        j = j - 1
        score += sim_mat[string_to_num(seq1[i - 1]),
                         string_to_num(seq2[j - 1])]
    elif D[i, j] - gap_score == D[i - 1, j]:
        seq1_aln = seq1[i - 1] + seq1_aln
        seq2_aln = '-' + seq2_aln
        i = i - 1
        score += gap_score
    else:
        seq1_aln = '-' + seq1_aln
        seq2_aln = seq2[j - 1] + seq2_aln
        j = j - 1
        score += gap_score

if j > 0:
    while j > 0:
        seq1_aln = seq1[j-1] + seq1_aln
        seq2_aln = '-' + seq2_aln
        j = j - 1
        score += gap_score
if i > 0:
    while i > 0:
        seq1_aln = '-' + seq1_aln
        seq2_aln = seq2[i-1] + seq2_aln
        i = i - 1
        score += gap_score

print("The optimal alignment_matrix has a score %s" % score)
print(seq1_aln + '\n' + seq2_aln)