# https://www.youtube.com/watch?v=OSGv2VnC0go
names = ['Shaun', 'Sarah', 'Finley']
colors = ['red', 'green', 'yellow', 'blue']


# foreach
for c in colors:
    print(c)


# loop backwards
for c in reversed(colors):
    print(c)


# loop of index and item
for i, c in enumerate(colors):
    print(f" {i}, '-->', {colors[i]}")


# loop over 2 collections
for name, color in zip(names, colors):
    print(name, '-->', color)


# sorted
for c in sorted(colors):
    print(c)


# sorted in reverse
for c in sorted(colors, reverse=True):
    print(c)


# custom sort
print(sorted(colors, key=len))


# call function until sentinel value
# e.g.
# blocks = []
# while True:
#     block = f.read(32)
#     if block == '':
#         break
#     blocks.append(block)

# blocks = []
# for block in iter(partial(f.read, 32), ''):
#     blocks.append(block)


# distinguishing multiple exit points
def find(seq, target):
    for i, value in enumerate(seq):
        if value == tgt:
            break
    # for-else nothing is found
    # no-break
    else:
        return -1

    return i


