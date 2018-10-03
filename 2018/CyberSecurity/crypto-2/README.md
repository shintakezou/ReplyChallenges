# Please don't RFC

Here we have a capture of packets from an IP to another. I've opened
it in [Wireshark](https://www.wireshark.org/). Scrolling the packets
you can easily spot informations: a base64 string and a (RSA) public
key.

Hypothesis: the base64 string is a message encrypted (well, this is
stated somewhere) with the public key.

Inspecting the public key with openssl,

    openssl rsa -pubin -in public_key.txt -text

I see that it's a 1046 bit key. That is, it is possible to “crack” it
in order to obtain the private key which can be used to decrypt the
message.

So I've taken the modulus and used this:

- http://factordb.com/

to find its factors. Now, unfortunately I don't know more than this
about the topic, so I googled for how I can generate a private key
having the factors of the modulus, and found this:

- https://0day.work/how-i-recovered-your-private-key-or-why-small-keys-are-bad/

so that now I have [the code to generate the private key](priv_exp.py)
cooked nicely in its PEM form. (I've called the output
`priv_key.asc`).

Now we can try this:

    openssl rsautl -decrypt \
	  -inkey priv_key.asc -in <(base64 -d encrypted_b64.txt)

The `encrypted_b64.txt` is the base64 string we found in the packets.

It doesn't work:

> padding check failed:rsa_eay.c:602

When such things happen you might question everything you've done so
far, and you also ask yourself if there's something you missed. I have
wasted time digging more deeply the packets, I believed there should be
some clue I missed.

Lesson learned (maybe): the first thing to do is to check if the
private key is correct — I did, but after having wasted time following
other paths. From a private key you can extract the public key (it's a
regular thing, you do it with openssl). Done, and it matches with the
public key found in the packets, so the private key is correct.

Then, read what a program has to say, and think about it: there's
something wrong with the *padding*, so maybe you need to play a little
bit with it. If you try `-raw`, you obtain garbage. The default
(PKCS#1) isn't good, as seen above. But if you try `-oaep` (that is,
[optimal asymmetric encryption padding](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding)),
**bingo**.

