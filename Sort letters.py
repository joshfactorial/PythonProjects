import itertools
im

Str1 = "G"
Str2 = "R"
letters = ['G', "S", "O", "A", "R", "O"]

letters.remove(Str1)
perms1 = list(itertools.permutations(letters))
for item in perms1:
    print(Str1 + item)

letters = ['G', "S", "O", "A", "R", "O"]
letters.remove(Str2)
perms2 = list(itertools.permutations(letters))
for item in perms2:
    print(Str2 + item)