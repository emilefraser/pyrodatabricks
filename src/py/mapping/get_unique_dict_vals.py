# in[0]
# description

# out[0]
## Using set() + values() + dictionary comprehension
# Get Unique values from list of dictionary
res = list(set(val for dic in test_list for val in dic.values()))

# Using set() + values() + from_iterable()
# Get Unique values from list of dictionary
res = list(set(chain.from_iterable(sub.values() for sub in test_list)))

res=[]
for i in test_list:
    res.extend(list(i.values()))
res=list(set(res))

# Using Counter() + set()
# Get Unique values from list of dictionary
res = list(set(val for sub in test_list for val in Counter(sub).values()))

