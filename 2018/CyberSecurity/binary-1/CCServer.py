import mala

#xor_key = "d3cRYp7_k3Y"
#hostname = ""

a = [31,
     117,
     47,
     21,
     99,
     32,
     88,
     110,
     5,
     71,
     54,
     2,
     112,
     12,
     60,
     45,
     2,
     7,
     51,
     69,
     80,
     52,
     25]


c = mala.CCServer(a)
print c.decrypt_hostname()



