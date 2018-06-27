clusters = [('seq1',), ('seq2',), ('seq3',), ('seq4',), ('seq5',)]
merges = (('seq3',), ('seq4',))
temp_subcluster = ()
for items in [merges][-1]:
    if type(items) is tuple:
        for elements in items:
            temp_subcluster += (elements,)  # merge sub sub clusters into one
    else:
        temp_subcluster += (items,)