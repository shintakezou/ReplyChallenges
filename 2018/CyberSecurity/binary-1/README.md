# Malware in the bottle

The given file has extension `.bin` but file tells us that it is a
Python 2.7 byte compiled binary. This is allegedly a malaware. And the
purpose is to obtain the hostname of the Command & Control server.

A [simple script](disasme.py) can dump the opcodes, so that we can see
what's inside.

You can swiftly see that there are two classes, `CCServer` and `Bot`.

Then, this

    76  50 LOAD_NAME                3 (__name__)
        53 LOAD_CONST               6 ('__main__')
        56 COMPARE_OP               2 (==)
        59 POP_JUMP_IF_FALSE      174

is the classical

```python
if __name__ == '__main__':
    do_something()
```

As first thing of the *do something* part, a list is build, and this
list's name is `hostname`. 

    77     62 LOAD_CONST    7 (31)
           65 LOAD_CONST    8 (117)
           68 LOAD_CONST    9 (47)
           71 LOAD_CONST   10 (21)
           74 LOAD_CONST   11 (99)
           77 LOAD_CONST   12 (32)
		   ...

Which is rather interesting for us. Then the class `CCServer` is
instantiated passing the `hostname` as first argument:

    80      137 LOAD_NAME         1 (CCServer)
            140 LOAD_NAME         4 (hostname)
            143 CALL_FUNCTION     1
            146 STORE_NAME        5 (server)
			
That is,

```python
server = CCServer(hostname)
```

The built list is

```python
hostname = [31, 117, 47, 21, 99, 32, 88, 110, 5, 71,
            54, 2, 112, 12, 60, 45, 2, 7, 51, 69, 80,
            52, 25]
```

We can't obtain a string from this list (there are 5, 2, 7, …): likely
it is crypted and the key to decrypt it is into CCServer.

Let's see what's inside it using the Python REPL. (I have renamed the
file as `mala.pyc`)

```
>>> import dis
>>> import mala
>>> dis.dis(mala.CCServer)
```

In its `__init__` we see this

    7  0 LOAD_CONST  	1 ('d3cRYp7_k3Y')
	   3 LOAD_FAST		0 (self)
	   6 STORE_ATTR		0 (xor_key)

That is

```python
xor_key = 'd3cRYp7_k3Y'
```

Then we see a method called `decrypt_hostname`, which is rather
self-explanatory, and it ends returning a value. Let's assume it's the
plain hostname (`plain_host`).

Let's try it… it is done in [CCServer.py](CCServer.py), and the output
proves the hypothesis right.


## Note

In order to run `disasme.py` and `CCServer.py`, you need `mala.pyc`,
which is nothing but the file given for the challenge, renamed. I
don't include it, as usual.
