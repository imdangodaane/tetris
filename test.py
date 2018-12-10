#!/usr/bin/env python3

def rotate(m):
    b = list(zip(*reversed(m)))
    for i in range(len(b)):
        b[i] = list(b[i])
    for i in b:
        print(i)
    return b

rotate([
 [0, 1, 1],
 [1, 1, 0]
])
rotate([
[0, 1],
[0, 1],
[1, 1]
])
