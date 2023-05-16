from collections import deque
colors = ['red', 'green', 'yellow', 'red', 'black']
# bad
del colors[0]
colors.pop(0)
colors.insert(0, 'purple')
print(colors)
# fast
colors = deque(['red', 'green', 'yellow', 'red', 'black'])
colors.popleft()
colors.appendleft('purple')