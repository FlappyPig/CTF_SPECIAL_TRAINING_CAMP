m="d8dc053d372d0690194553d7ffbed36750703f417bcb989f98b181a07203ec4807e239df7f4dd9f983cc8d5081b8f7673e7b9ea32b51".decode("hex")
c="f55847d90055888b420b5e3921f3697a63fe88e6c6541a8e53e58cd89e1702c45498b45b57516feb01925de8fa9e359ce226ed1aa5be".decode("hex")
c2="6c5c2c047a3a59dceb196ebad9dd9e98055e3f0325f0891e783010ff2a1885f2702a009f655e649bf4d7b3811c20a75bbc1d84c3a8c7".decode("hex")

def xor(a,b):
    assert len(a)==len(b)
    c=""
    for i in range(len(a)):
        c+=chr(ord(a[i])^ord(b[i]))
    return c

fR=xor(xor(c[0:27],m[27:54]),c2[0:27])
print xor(xor(xor(xor(c[27:54],m[0:27]),m[27:54]),c2[27:54]),fR)+fR