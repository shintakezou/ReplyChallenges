#! /usr/bin/python3

# https://github.com/AChep/SudokuSolver/blob/master/sudoku.py
from sudoku import Sudoku
import hashlib

sha = hashlib.sha256()

s = ""

with open("trascritto") as f:
    # the Sudoku Solver uses 0 as missing number, we have . and numbers from 0 to 15.
    # therefore the numbers in input are incremented by 1, and . is replaced with 0
    for line in f:
        a = map(lambda x: "0" if x=='.' else str(int(x,16)+1), list(line.rstrip()))
        s += " ".join(a) + "\n" # .rstrip()
    f.close()

print(s)
r = Sudoku(s.rstrip())

risolto = r.solve() # we suppose "risolto" (solved) is True

r0 = Sudoku.format(r.solution)
r1 = [x.split() for x in r0.split('\n')]

fin0 = "".join(["%X" % (int(i)-1) for l in r1 for i in l])
sha.update(bytes(fin0, 'utf-8'))
print(sha.hexdigest())

#print(r.solution)

