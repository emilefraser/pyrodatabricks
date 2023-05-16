p = "Raymond", "Hettinger", 0x30, "python@example.com"
fname, lname, age, email = p

# updating multiple states
def fibonacci(n):
    x = 0
    y = 1
    for i in range(n):
        print(x)
        t = y
        y = x + y # rquires intermediate state, ordering is important
        x = t

# unpacking allows to calculated as a pure higher level calculation
def fibonacci(n):
    x, y = 0, 1
    for i in range(n):
        print(x)
        x, y = y, x+y
