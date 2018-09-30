# Stranger code

The given zip archive contains two files: an html file and javascript
code. The html calls a javascript function when you click
“submit”. Once you beautify `blob.js`, you can easily read a function
called `flag()` which builds a string which is output when you insert
the correct password, which is again built at the beginning of the
function `magic()`. All you need is to “interpret” `flag()`: knowing
the password which unlock the magic is a waste of time.

It's very hard to spot all this if you don't beautify properly the
blob!

I've used this:

- [Online JavaScript Beautifier](https://beautifier.io/)

When you have a clean and clear javascript code, it becomes very
easy. Yet, you don't want to make too many calculation, you are lazy,
so you add

    console.log(flag())
	
at the end of the unobfuscated script and you run it in nodejs,
obtaining the flag as output.
