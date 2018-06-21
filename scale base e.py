import numpy as np

'''
d = distance from the nut
s = scale length
n = fret number
'''


def cal_frets(scale):
    distances_normal = []
    distances_natural = []
    for i in range(18):
        distances_natural.append(scale-(scale/(np.exp((i+1)/13))))
    for i in range(24):
        distances_normal.append(scale-(scale/(2**((i+1)/12))))
    return distances_natural, distances_normal


natural, normal = cal_frets(25.5)
print("natural log scale")
print(" in\n".join(map(str, natural)))
