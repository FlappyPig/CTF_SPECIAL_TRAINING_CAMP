s="flag"
print s.encode("hex")

s="flag"
t=s.encode("hex")
print int(t,16)

print int("a".encode("hex"),16)
print ord("a")

num=584734024210391580014049650557280915516226103165
print hex(num)
print hex(num)[2:-1]
print hex(num)[2:-1].decode("hex")

def num2str(num):
    tmp=hex(num)[2:].replace("L","")
    if len(tmp) % 2 == 0:
        return tmp.decode("hex")
    else:
        return ("0"+tmp).decode("hex")
print num2str(584734024210391580014049650557280915516226103165)

from Crypto.Util.number import long_to_bytes,bytes_to_long
flag="flag{123}"
print bytes_to_long(flag)
print long_to_bytes(bytes_to_long(flag))

import urllib
print urllib.quote("flag{url_encode_1234_!@#$}")
d = {'name':'bibi@flappypig.club','flag':'flag{url_encode_1234_!@#$}'}
print urllib.urlencode(d)

import base64
print "flag".encode("base64")
print base64.b16encode("flag")
print base64.b32encode("flag")
print base64.b64encode("flag")

print "ZmxhZw==".decode("base64")
print base64.b16decode("666C6167")
print base64.b32decode("MZWGCZY=")
print base64.b64decode("ZmxhZw==")