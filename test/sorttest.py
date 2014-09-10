#!/usr/bin/python

class App:
    name = ''
    rank = 32767

    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

if __name__ == "__main__":

    applist_orig = []
    applist_orig.append(App('a',1))
    applist_orig.append(App('b',3))
    applist_orig.append(App('c',2))

    cmp_func_by_rank = lambda a, b: cmp(a.rank,b.rank)
    applist_sorted = sorted(applist_orig, cmp_func_by_rank, reverse=False)

    for app in applist_sorted:
        print app.name, "   ", app.rank