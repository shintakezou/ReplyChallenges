import marshal
import dis

with open("mala.pyc") as f:
    magic = f.read(4)
    date = f.read(4)
    c = marshal.load(f)
    f.close()
    dis.dis(c)

    
