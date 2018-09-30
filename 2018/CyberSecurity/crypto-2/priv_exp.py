#! /usr/bin/python3
import pyasn1.codec.der.encoder
import pyasn1.type.univ
import base64

# exponent and modulus of the public key
e = 0x010001
n = 0x2A56ACE821C382A3E1F9B9453F0F812E8853CE70AE8A8496376F07FC7E84403542F013A46BD565C3AA9AC88233EDC175B71B96C6C648714D49863FC22B1052D5075A8E48D7B4D8D415F48EB6AAAEF425E592D663921ED3133A345DF48312E5632F802B0006FCFAF27DC946986A414E2C3F24C34D174873E92D0CF810607D3E7C48E53D

# factors of the modulus
p = 3133337
q = 159193242584121369256956316628736688489554176208962477712437848125631300025580723764883651750886123395688239147448549549830059185022196717465966721467382854991929100850081341277904771865807748063475639850686489536299234645327870095249165664682217064183144557295339759807052960224740996236995810215803918227781

# see https://0day.work/how-i-recovered-your-private-key-or-why-small-keys-are-bad/

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

phi = (p-1)*(q-1)
d = modinv(e,phi)

dp = modinv(e,(p-1))
dq = modinv(e,(q-1))
qi = modinv(q,p)

def pempriv(n, e, d, p, q, dP, dQ, qInv):
    template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    seq = pyasn1.type.univ.Sequence()
    for x in [0, n, e, d, p, q, dP, dQ, qInv]:
        seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))
    der = pyasn1.codec.der.encoder.encode(seq)
    return template.format(base64.encodestring(der).decode('ascii'))

key = pempriv(n,e,d,p,q,dp,dq,qi)

print(key)
