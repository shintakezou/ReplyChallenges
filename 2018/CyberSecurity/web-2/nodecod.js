var CryptoJS = require('crypto-js')

for (i = 0; i < 256; i++) {
    var k = CryptoJS.SHA256("\x93\x39\x02\x49\x83\x02\x82\xf3\x23\xf8\xd3\x13"+String.fromCharCode(i));
    var the_key = CryptoJS.enc.Hex.parse(k.toString().substring(0,32))
    var the_iv = CryptoJS.enc.Hex.parse(k.toString().substring(32,64));

    var b64enc="PKhuCrfh3RUw4vie3OMa8z4kcww1i7198ly0Q4rpuyA=";
    var enc = CryptoJS.AES.decrypt(b64enc, //CryptoJS.enc.Base64.parse(b64enc).toString(),
				   the_key,
				   { iv: the_iv });

    try {
	var forse = enc.toString(CryptoJS.enc.Utf8);
	if (forse) {
	    console.log(i + " <<<" + enc.toString(CryptoJS.enc.Utf8) + ">>>");
	}
    } catch(e) {
	//console.log(e)
    }
}
