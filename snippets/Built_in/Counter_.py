from collections import Counter


def solution(participant, completion):
    answer = Counter(participant) - Counter(completion)
    return list(answer.keys())[0]


c = Counter()                           # a new, empty counter
c = Counter('gallahad')                 # a new counter from an iterable
c = Counter({'red': 4, 'blue': 2})      # a new counter from a mapping
c = Counter(cats=4, dogs=8)             # a new counter from keyword args

# ===
c = Counter(['eggs', 'ham'])
print(c['bacon'])  # 0 (count of a missing element is zero)

# ===
c.total()                       # total of all counts
c.clear()                       # reset all counts
list(c)                         # list unique elements
set(c)                          # convert to a set
dict(c)                         # convert to a regular dictionary
c.items()                       # convert to a list of (elem, cnt) pairs
Counter(dict("list_of_pairs"))    # convert from a list of (elem, cnt) pairs
c.most_common()[:-n-1:-1]       # n least common elements
+c                              # remove zero and negative counts

# ===
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
c + d  # Counter({'a': 4, 'b': 3})  # add two counters together:  c[x] + d[x]
c - d  # Counter({'a': 2})          # subtract (keeping only positive counts)
c & d  # Counter({'a': 1, 'b': 1})  # intersection:  min(c[x], d[x])
c | d  # Counter({'a': 3, 'b': 2})  # union:  max(c[x], d[x])
print(c == d)  # False              # equality:  c[x] == d[x]
print(c <= d)  # False              # inclusion:  c[x] <= d[x]

# ===
c = Counter(a=2, b=-4)
print(+c)  # Counter({'a': 2})
print(-c)  # Counter({'b': 4})
