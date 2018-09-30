# Great host

The given file is an executable. Luckly a GNU+Linux ELF executable
(elf32-i386). In a real situation you shouldn't run it without
precautions. Anyway…

I tried to run it under gdb, but it can't be done because the code
check to see if it is running under a debugger. Hence the first thing
is to remove this annoying check!

This check is done using `ptrace`. I've used this:

    objdump -D
	
to take a look at some code. Search for where `ptrace` is called:

    80485a9: e8 e2 fe ff ff call   8048490 <ptrace@plt>
    80485ae: 83 c4 10       add    $0x10,%esp
    80485b1: 83 f8 ff       cmp    $0xffffffff,%eax
    80485b4: 75 1a          jne    80485d0
    80485b6: 83 ec 0c       sub    $0xc,%esp
    80485b9: 68 20 89 04 08 push   $0x8048920 ; "No debugger please!"
    80485be: e8 5d fe ff ff call   8048420 <puts@plt>

I've changed `75 1a` (jne) into `74 1a` (je), so that now the code
runs only under a debugger.

The file [wysiNwyg-okdebug.patch](wysiNwyg-okdebug.patch) is a patch
to be applied to the uuencoded executable file (and then you have to
uudecode it, of course).

Now you can run it in gdb and see that it prints few lines and then
ask for a password. Breaking (ctrl-c) at this point leaves us into a
system call, the one waiting for input, which we aren't interested
in. Let's backtrace to see that likely the frame 8 is what we want:

    (gdb) frame 8
	(gdb) break
	(gdb) cont

We reach the address 0x80487ea, which is just after a call to a
`fgets`. Keeping an eye to the output of `objdump -D`, you see
what's coming next (also, `display/10i $eip` helps…)

It checks if the last character read is a newline and replaces it with
a 0.

Going on with `nexti` (or by eye if you are reading the code rather
done tracing it), we see a promising `strcmp` between whatever was
read by `fgets` and another string at 0x8048a73; `x/s` this address to
see `s3cR3t_p4sSw0rD`. It smells trick because you can spot this
string with `strings` (which of course I've run as first thing),
followed by another string, *This is not the solution you are looking
for :)*, and guess what's at 0x8048a84, argument of the upcoming
`puts`?

    => 0x8048830:   push   $0x8048a73
       0x8048835:   push   $0x8049d60
       0x804883a:   call   0x80483f0 <strcmp@plt>
       0x804883f:   add    $0x10,%esp
       0x8048842:   test   %eax,%eax
       0x8048844:   jne    0x8048858
       0x8048846:   sub    $0xc,%esp
       0x8048849:   push   $0x8048a84
       0x804884e:   call   0x8048420 <puts@plt>
       0x8048853:   add    $0x10,%esp

So the interesting branch is the one at 0x8048858, where it checks
to see if the length of the given password is 34. If it is… it exits
without saying *try again*… We've got nothing, though: the good
things must have happened before.

Thus I went up (in the source, lazy approach) to see what's before the
`fgets` call, until I saw a series of `movb` which are suspicious,
they look something like there's a string which is built by code byte
after byte. That's a more interesting point to step on, and so I did:
breakpoint at 0x80486e9, and then a little bit of inspection here and
there to see what was around.

To cut the story short, you see a loop where bytes from the input
buffer are xorred with 0x33 and compared with bytes taken from
elsewhere and put into edx. So now we know that our password is there,
hidden by a xor 0x33.

    lea    -0x2f(%ebp),%edx

There's our data. So after the stop at the breakpoint at 0x80486e9, I
did `x/34xb $ebp-0x2f` to see those bytes.

There are many ways you can xor them with 0x33, even staying in gdb,
e.g., using [gef](https://gef.readthedocs.io/en/master/), and more
exactly `xor-memory`, something like

    xor-memory display ($ebp-0x2f) 34 0x33

Anyway it doesn't matter how you do that: you will read the password,
which is

    1n1T_4nD_F1n1_4rR4Ys_4r3_S0_34sY!!

Now you can unzip the zip and take the flag.
