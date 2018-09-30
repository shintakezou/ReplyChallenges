# Type it

There's a non-standard HTML file containing a bare form where the
submit button calls the javascript function `auth()`.

When the username is `h4ck3r`, the given password is AES encrypted and
compared with a base64 representation of the AES encrypted correct
password:

    PKhuCrfh3RUw4vie3OMa8z4kcww1i7198ly0Q4rpuyA=

We also have the key and initial vector used for the AES encryption,
so we have all we need to decrypt this to have the clear password. Key
and IV are taken form a SHA256 of a string which is written inside the
code itself! It would have been too easy without a missing character in
the string used to generate the SHA256.

We have to try only 256 different strings… But only fews seem good,
and only one is the correct one. Since it's javascript, I've used
NodeJS (after `npm install crypto-js`):

- [nodecod.js](nodecod.js)
