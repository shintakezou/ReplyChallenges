# Hexadoku

Basically the problem is to solve a sudoku where numbers can go from 0
to 15, hence hexadoku. The algorithm is the same of a regular sudoku,
so I searched for an already cooked implementation, general enough to
handle a grid of different size.

I've used this one:

- [Sudoku solver](https://github.com/AChep/SudokuSolver)

The file [trascritto](trascritto) is the “transcript” of the content
of the image. The most boring part was to transcribe the image; likely
this step can be done automatically, too, but anyway I did it by hand.

The code [solvisudoku.py](solvisudoku.py) is a Python (3) script which
adapts the input so that the AChep's SudokuSolver can do its job.

