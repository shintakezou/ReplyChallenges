#! /usr/bin/python3
import hashlib

sha = hashlib.sha256()

dname = 'dictionary.txt'
sname = 'scrambled-words.txt'

dlen = {}

def wsorted(ws):
    """Sort the letters of a word"""
    w = list(ws.rstrip())
    w.sort()
    return ''.join(w)

def k(ws):
    """Compute a (hopefully unique) key for a word"""
    w = ws.rstrip()
    return str(len(w)) + ";" + str(wsorted(w))

with open(dname, 'r') as f:
    for ws in f:
        w = ws.rstrip()
        if k(w) in dlen:
            print("COLLISION: %s (< %s)" % (w, dlen[k(w)]))
        dlen[k(w)] = w
    f.close()

wlist = []

with open(sname, 'r') as f:
    for ws in f:
        w = ws.rstrip()
        wlist.append(dlen[k(w)].encode('utf-8'))
    f.close()

sha.update(b''.join(wlist))

# i.e., "{FLG:%s}" % (sha.hexdigest())
print(sha.hexdigest())
