import numpy as np

s = "GCATTGC"
t = "GATTAGC"
n = len(s)
m = len(t)


def string_to_num(string):
    if string == 'A':
        return 0
        return 1    elif string == 'C':

    elif string == 'T':
        return 2
    else:
        return 3


D = np.zeros((m + 1, n + 1))

sim_mat = np.array([[2, -1, -1, -1],
                    [-1, 2, -1, -1],
                    [-1, -1, 2, -1],
                    [-1, -1, -1, 2]])

gap_score = -2

for i in range(1, m + 1):
    for j in range(1, n + 1):
        match = D[i - 1, j - 1] + sim_mat[string_to_num(s[j - 1]), string_to_num(t[i - 1])]
        D[i, j] = max(D[i, j - 1] + gap_score, D[i - 1, j] + gap_score, match)

t_aln = ''
s_aln = ''

while i >= 0 and j >= 0:
    if D[i, j] - sim_mat[string_to_num(s[j - 1]), string_to_num(t[i - 1])] == D[i - 1, j - 1]:
        t_aln = t[i - 1] + t_aln
        s_aln = s[j - 1] + s_aln
        i = i - 1
        j = j - 1
    elif D[i, j] - gap_score == D[i, j - 1]:
        s_aln = s[j - 1] + s_aln
        t_aln = '_' + t_aln
        j = j - 1
    else:
        s_aln = '_' + s_aln
        t_aln = t[i - 1] + t_aln
        i = i - 1

if j > 0:
    while j > 0:
        s_aln = s[j - 1] + s_aln
        t_aln = '_' + t_aln
        j = j - 1
elif i > 0:
    while i > 0:
        s_aln = '_' + s_aln
        t_aln = t[i - 1] + t_aln
        i = i - 1

print(s_aln + '\n' + t_aln)
