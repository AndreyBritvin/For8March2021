"""a = {"a":[["", ""],""], "b":[["", ""],""], "c":[["", ""],""]}
a['b  \n Solved by Andrey'] = a['b']
del a['b']
print(a)"""

a = {
    "a":[123,456],
    "b":[789]
}
for i in list(a.keys()):
    try:
        a[i].remove(456)
    except ValueError:
        continue

print(a)