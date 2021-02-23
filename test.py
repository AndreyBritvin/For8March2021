"""a = {"a":[["", ""],""], "b":[["", ""],""], "c":[["", ""],""]}
a['b  \n Solved by Andrey'] = a['b']
del a['b']
print(a)

a = {
    "a":[123,456],
    "b":[789]
}
for i in list(a.keys()):
    try:
        a[i].remove(456)
    except ValueError:
        continue
a = [0,1]"""
a = {2: 'hh1', 1:"hhh2"}
#s = list(a.keys())#.sort(reverse=True)
s = [2,3,4,1]
s.sort()
print(s)