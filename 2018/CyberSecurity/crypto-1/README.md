# Warmap

The file `WarMap.txt` is made of several lines, each line has an
encoded string. The encoding is base64. Decoding it with

    base64 -d -i <WarMap.txt >bytes.txt
	
you see “bytes” written in base 2. I have tried this with Python
(REPL):

    >>> f=open("bytes.txt")
    >>> c=f.read(
    >>> d=[chr(int(x,2)) for x in c.split(" ")]
    >>> "".join(d)

The output contains the solution.
