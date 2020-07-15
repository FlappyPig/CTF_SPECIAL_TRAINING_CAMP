def caesar_decrypt(c,k):
    r=""
    for i in c:
        r+=chr((ord(i)-k)%128)
    return r

def caesar_brute(c,match_str):
    result=[]
    for k in range(128):
        tmp=caesar_decrypt(c,k)
        print tmp
        if match_str in tmp:
            result.append(tmp)
    return result

c="bXNobgJyaHB6aHRwdGgE".decode("base64")
print caesar_brute(c,"flag")
