# Joshua Allen
# 676067230
# final project
# I used http://www.srmuniv.ac.in/sites/default/files/files/1(7).pdf as a guide for writing the program
# and https://www.youtube.com/watch?v=AGSuDxQ7gP8 for help with the neighbor-joining algorithm


import numpy as np
import glob
import pandas as pd


def read_seq(file) -> (str, str):
    # Read in file, which is a simple amino acid string, then
    # making it all upper case for consistency
    # also uses the FASTA header as a name, which will become the index for the dataframe
    name = ""
    with open(file) as file:
        seq = file.readline().rstrip('\n')
        if seq[0] == '>':
            name = seq[1:]
            seq = ''
        else:
            seq = file.readline().rstrip('\n').upper().replace(" ", "")
        for line in file:
            seq += line.rstrip('\n').upper().replace(" ", "")
    return name, seq


def align_multiple(matrix, clust1: list, clust2: list, yay=0) -> (pd.DataFrame, float):
    # Align two clusters of sequences in a matrix of sequences
    # and return the matrix with the chosen clusters aligned
    # works for 2 sequences up to theoretically as many as you want.
    clustal1 = []
    clustal2 = []
    for seqs in clust1:
        clustal1.append(matrix.loc[[seqs]].values.tolist()[0][0])
    for seqs in clust2:
        clustal2.append(matrix.loc[[seqs]].values.tolist()[0][0])
    m = len(clustal1[0])
    n = len(clustal2[0])

    # initialize scoring matrix
    dpmat = np.zeros((m + 1, n + 1), dtype=float)
    moves = np.zeros((m + 1, n + 1), dtype=int)

    # scores at the edges
    # for ind in range(1, m + 1):
    #     dpmat[ind, 0] = dpmat[ind - 1, 0] + gap_score
    #
    # for jind in range(1, n + 1):
    #     dpmat[0, jind] = dpmat[0, jind - 1] + gap_score

    # Dynamic programming algorithm. The main modification is it finds the average score for multiple sequences.
    for k in range(1, m + 1):
        for l in range(1, n + 1):
            total = 0
            for p in range(len(clustal1)):
                for q in range(len(clustal2)):
                    total += blosum62[clustal1[p][k-1]][clustal2[q][l-1]]
            match = dpmat[k - 1, l - 1] + total/(len(clustal1)*len(clustal2))
            if moves[k, l-1] == 2:
                gap2 = dpmat[k, l-1] + gap_continue
            else:
                gap2 = dpmat[k, l-1] + gap_score
            if moves[k-1, l] == 3:
                gap3 = dpmat[k-1, l] + gap_continue
            else:
                gap3 = dpmat[k-1, l] + gap_score
            temp = max(gap2, gap3, match)
            dpmat[k, l] = temp
            if dpmat[k, l] == match:
                moves[k, l] = 1
            elif dpmat[k, l] == gap2:
                moves[k, l] = 2
            else:
                moves[k, l] = 3

    s, t = np.unravel_index(dpmat.argmax(), dpmat.shape)
    v = m
    w = n

    if yay == 0:
        # Reverse trace, activates only if the function call declares no integer or declares 0. Default is 0.
        # Initialize the alignment_matrix clusters
        mod1 = ['' for x in range(len(clustal1))]
        mod2 = ['' for y in range(len(clustal2))]
        while v > s:
            for p in range(len(clustal1)):
                mod1[p] = clustal1[p][v-1] + mod1[p]
            for q in range(len(clustal2)):
                mod2[q] = '-' + mod2[q]
            v -= 1
        while w > t:
            for p in range(len(clustal1)):
                mod1[p] = '-' + mod1[p]
            for q in range(len(clustal2)):
                mod2[q] = clustal2[q][w - 1] + mod2[q]
            w -= 1
        while s > 0 and t > 0:
            if moves[s, t] == 1:
                for p in range(len(clustal1)):
                    mod1[p] = clustal1[p][s-1] + mod1[p]
                for q in range(len(clustal2)):
                    mod2[q] = clustal2[q][t-1] + mod2[q]
                s -= 1
                t -= 1
            elif moves[s, t] == 2:
                for p in range(len(clustal1)):
                    mod1[p] = '-' + mod1[p]
                for q in range(len(clustal2)):
                    mod2[q] = clustal2[q][t - 1] + mod2[q]
                t -= 1
            else:
                for p in range(len(clustal1)):
                    mod1[p] = clustal1[p][s - 1] + mod1[p]
                for q in range(len(clustal2)):
                    mod2[q] = '-' + mod2[q]
                s -= 1
        # Tacks gaps onto the beginning if the sequences aren't complete.
        while t > 0:
            for p in range(len(clustal1)):
                mod1[p] = '-' + mod1[p]
            for q in range(len(clustal2)):
                mod2[q] = clustal2[q][t - 1] + mod2[q]
            t -= 1
        while s > 0:
            for p in range(len(clustal1)):
                mod1[p] = clustal1[p][s-1] + mod1[p]
            for q in range(len(clustal2)):
                mod2[q] = '-' + mod2[q]
            s -= 1
        # Inserts new alignment into the original matrix
        i_x = j_y = 0
        for index1 in clust1:
            matrix.loc[index1:index1] = mod1[i_x]
            i_x += 1
        for index2 in clust2:
            matrix.loc[index2:index2] = mod2[j_y]
            j_y += 1
        return matrix
    else:
        # returns score only if the matrix alignment was skipped.
        return np.amax(dpmat)


def merge_clusters(name_list, merge_tuple):
    # merges clusters
    temp_subcluster = ()
    temp_cluster = []
    for item in name_list:
        flag = 0
        for element in merge_tuple:
            if item == element:
                temp_subcluster += (item,)
                flag = 1  # if it's one we're supposed to merge, add to cluster
        if flag == 0:
            temp_cluster.append(item)  # if it's not add it to the main cluster
    temp_cluster.append(temp_subcluster)
    return temp_cluster


def unstack_tuple(merge: tuple) -> list:
    # Recursive function that turns tuple into a simple list for the purposes of performing the alignment.
    if type(merge) is str:
        return [merge]
    else:
        temp_list = []
        for element in merge:
            if type(element) is str:
                temp_list.append(element)
            else:
                holder = unstack_tuple(element)
                for part in holder:
                    temp_list.append(part)
        return sorted(temp_list)


def determine_merges(matrix, length):
    # Determines which two clusters will be merged based on the clustal algorithm
    # which uses a modified form of neighbor-joining. The original algorithm calls for minimizing the score, but
    # since my dynamic programming algorithm rates closer matches higher, so I used the maximum, and added the distances
    # between the clusters.
    u = []
    for column in matrix:
        u.append(matrix[column].sum())
    u = pd.DataFrame(u, index=matrix.index)  # set up u vector
    scoring_matrix = [[0]*len(matrix) for x in range(len(matrix))]  # create emtpy scoring matrix
    scoring_matrix = pd.DataFrame(scoring_matrix, index=matrix.index, columns=matrix.index)
    for column in matrix:  # fill out matrix according to neighbor-joining algorithm
        for row_temp in matrix:
            if row_temp == column:
                pass
            elif scoring_matrix[row_temp][column] != 0:
                scoring_matrix[column][row_temp] = scoring_matrix[row_temp][column]
            else:
                scoring_matrix[column][row_temp] = (length-2)*(matrix[column][row_temp]) + u[0][row_temp] + u[0][column]
    # return the maximum (since our scoring matrix was maximum = best match)
    return scoring_matrix[scoring_matrix == max(scoring_matrix[new_scores != 0].max())].stack().dropna().index[0]


def calculate_new_matrix(matrix: pd.DataFrame, clust_names: list) -> pd.DataFrame:
    # Uses the new clusters to calculate the new scoring matrix that will be used for the next cluster assignment
    new_matrix = [[0.0] * len(clust_names) for x in range(len(clust_names))]
    new_matrix = pd.DataFrame(new_matrix, index=clust_names, columns=clust_names)
    for column in new_matrix:
        for row_tem in new_matrix:
            if row_tem == column:
                pass
            elif type(row_tem) is tuple:
                if row_tem not in matrix.index.tolist():
                    temp_sum = 0.0
                    for tuplepart in row_tem:
                        temp_sum += matrix[column][tuplepart]
                    new_matrix[column][row_tem] = temp_sum / len(row_tem)
                else:
                    if new_matrix[row_tem][column] != 0:
                        new_matrix[column][row_tem] = new_matrix[row_tem][column]
                    else:
                        new_matrix[column][row_tem] = matrix[column][row_tem]
            else:
                if new_matrix[row_tem][column] != 0:
                    new_matrix[column][row_tem] = new_matrix[row_tem][column]
                else:
                    new_matrix[column][row_tem] = matrix[column][row_tem]
    return new_matrix


test_sequences = []
names = []
gap_score = -5
gap_continue = -1

'''
The blosum62 matrix includes a scoring column/row for "-" which will signify a gap in the alignment_matrix matrix
anything trying to align with a gap in the subcluster will be scored with the gap penalty
'''
blosum62 = pd.read_csv('C:/Users/Joshua/Google Drive/_grad school/Sp2018/cs466/BLOSUM62.csv', index_col=0)

'''
Read in the sequences as strings and names from the FASTA-formatted file. For simplicity, I declare the exact file
names here and put the files I need in the appropriate folder
'''
for fn in sorted(glob.glob("C:/Users/Joshua/Google Drive/_grad school/Sp2018/cs466/Sequences/*.dat")):
    temp = read_seq(fn)
    names.append(temp[0])
    test_sequences.append(temp[1])

'''
Creates an alignment matrix as a pandas dataframe, to take advantage of its indexing abilities 

'''
alignment_matrix = pd.DataFrame(test_sequences, index=names)

# Generate the initial scoring matrix
scores = []
for i in range(len(names)):
    row = []
    for j in range(len(names)):
        if i == j:
            row.append(0)
        else:
            # uses scoring feature of the multialign function, designated by the 1 at the end
            row.append(align_multiple(alignment_matrix, [names[i]], [names[j]], 1))
    scores.append(row)

# recasts scores matrix as a dataframe for indexing
scores = pd.DataFrame(scores, index=names, columns=names)

clusters = names  # initialize each sequence as a cluster itself
new_scores = [[0,30,50,10,30], [30,0,30,10,45], [50,30,0,10,30], [10,10,10,0,10], [30,45,30,10,0]] # new_scores will change but we may want to preserve the original
new_scores = pd.DataFrame(new_scores, index=names, columns=names)
'''
loop until there is only one cluster, in each loop, the new cluster set gets parsed and fed
into the multi-align function. Alignments are done treating each new cluster as one cluster and finding
the average score at each alignment_matrix column to determine which dynamic programming step to take.
'''
while len(clusters) > 1:
    # Find the max score for the matrix according to the clustal algorithm
    merges = determine_merges(new_scores, len(clusters))

    # recalculate the alignment_matrix with the cluster selected clusters
    cluster1 = merges[0]
    cluster2 = merges[1]
    cluster1 = unstack_tuple(cluster1)
    cluster2 = unstack_tuple(cluster2)
    alignment_matrix = align_multiple(alignment_matrix, cluster1, cluster2)

    # creates a new cluster list
    clusters = merge_clusters(clusters, merges)

    # calculates the new score based on the new cluster matrix
    new_scores = calculate_new_matrix(new_scores, clusters)  # calculates new scoring matrix for the cluster

pd.options.display.max_colwidth = 2000

# print(alignment_matrix)
i = 0
while i < (len(alignment_matrix.iloc[0].to_string())):
    print(alignment_matrix.index[0], '\t', alignment_matrix.iloc[0].to_string()[i:i + 60])
    print(alignment_matrix.index[1], '\t\t', alignment_matrix.iloc[1].to_string()[i:i + 60])
    print(alignment_matrix.index[2], '\t\t\t\t', alignment_matrix.iloc[2].to_string()[i:i + 60])
    print(alignment_matrix.index[3], '\t\t', alignment_matrix.iloc[3].to_string()[i:i + 60])
    print(alignment_matrix.index[4], '\t\t', alignment_matrix.iloc[4].to_string()[i:i + 60])
    print('\n')
    i += 60

print(merges)