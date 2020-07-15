#coding:utf-8
import urllib
from Crypto.Cipher import AES,DES
from Crypto.Util.number import long_to_bytes,bytes_to_long,getPrime,isPrime
import primefac
import gmpy2


alphabet_to_morse = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "Ä": ".-.-",
    "Ü": "..--",
    "ß": "...--..",
    "À": ".--.-",
    "È": ".-..-",
    "É": "..-..",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    ";": "-.-.-.",
    "?": "..--..",
    "-": "-....-",
    "_": "..--.-",
    "(": "-.--.",
    ")": "-.--.-",
    "'": ".----.",
    "=": "-...-",
    "+": ".-.-.",
    "/": "-..-.",
    "@": ".--.-.",
    "Ñ": "--.--",
    " ": " ",
    "": ""
}
morse_to_alphabet = {v: k for k, v in alphabet_to_morse.iteritems()}
def _morseremoveunusablecharacters(uncorrected_string):
    return filter(lambda char: char in alphabet_to_morse, uncorrected_string.upper())
def _playfair_2char_encode(tmp,map):
    for i in range(5):
        for j in range(5):
            if map[i][j] ==tmp[0]:
                ai=i
                aj=j
            if map[i][j] ==tmp[1]:
                bi=i
                bj=j
    if ai==bi:
        axi=ai
        bxi=bi
        axj=(aj+1)%5
        bxj=(bj+1)%5
    elif aj==bj:
        axj=aj
        bxj=bj
        axi=(ai+1)%5
        bxi=(bi+1)%5
    else:
        axi=ai
        axj=bj
        bxi=bi
        bxj=aj
    return map[axi][axj]+map[bxi][bxj]
def _playfair_2char_decode(tmp,map):
    for i in range(5):
        for j in range(5):
            if map[i][j] ==tmp[0]:
                ai=i
                aj=j
            if map[i][j] ==tmp[1]:
                bi=i
                bj=j
    if ai==bi:
        axi=ai
        bxi=bi
        axj=(aj-1)%5
        bxj=(bj-1)%5
    elif aj==bj:
        axj=aj
        bxj=bj
        axi=(ai-1)%5
        bxi=(bi-1)%5
    else:
        axi=ai
        axj=bj
        bxi=bi
        bxj=aj
    return map[axi][axj]+map[bxi][bxj]



def atbash_encode(m):
    alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    Origin=alphabet+alphabet.lower()
    TH_A=alphabet[::-1]
    TH_a=alphabet.lower()[::-1]
    TH=TH_A+TH_a
    r=""
    for i in m:
        tmp=Origin.find(i)
        if tmp!=-1:
            r+=TH[tmp]
        else:
            r+=i
    return r
def atbash_decode(c):
    return atbash_encode(c)
def urlencode(m):
    return urllib.quote(m)
def urldecode(c):
    return urllib.unquote(c)
def morseencode(decoded):
    """
    :param decoded:
    :return:
    """
    morsestring = []
    decoded = _morseremoveunusablecharacters(decoded)
    decoded = decoded.upper()
    words = decoded.split(" ")
    for word in words:
        letters = list(word)
        morseword = []
        for letter in letters:
            morseletter = alphabet_to_morse[letter]
            morseword.append(morseletter)
        word = "/".join(morseword)
        morsestring.append(word)
    return " ".join(morsestring)
def morsedecode(encoded):
    """
    :param encoded:
    :return:
    """
    characterstring = []
    words = encoded.split(" ")
    for word in words:
        letters = word.split("/")
        characterword = []
        for letter in letters:
            characterletter = morse_to_alphabet[letter]
            characterword.append(characterletter)
        word = "".join(characterword)
        characterstring.append(word)
    return " ".join(characterstring)
def shift_encrypt(m,k):
    l=len(k)
    c=""
    for i in range(0,len(m),l):
        tmp_c=[""]*l
        if i+l>len(m):
            tmp_m=m[i:]
        else:
            tmp_m=m[i:i+l]
        for kindex in range(len(tmp_m)):
            tmp_c[int(k[kindex])-1]=tmp_m[kindex]
        c+="".join(tmp_c)
    return c
def shift_decrypt(c,k):
    l=len(k)
    m=""
    for i in range(0,len(c),l):
        tmp_m=[""]*l
        if i+l>=len(c):
            tmp_c=c[i:]
            use=[]
            for kindex in range(len(tmp_c)):
                use.append(int(k[kindex]) - 1)
            use.sort()
            for kindex in range(len(tmp_c)):
                tmp_m[kindex] = tmp_c[use.index(int(k[kindex])-1)]
        else:
            tmp_c=c[i:i+l]
            for kindex in range(len(tmp_c)):
                tmp_m[kindex] = tmp_c[int(k[kindex]) - 1]
        m+="".join(tmp_m)
    return m
def zhalan_encrypt(m,k):
    chip=[]
    for i in range(0,len(m),k):
        if i+k>=len(m):
            tmp_m=m[i:]
        else:
            tmp_m=m[i:i+k]
        chip.append(tmp_m)
    c=""
    for i in range(k):
        for tmp_m in chip:
            if i < len(tmp_m):
                c+=tmp_m[i]
    return c
def zhalan_decrypt(c,k):
    l=len(c)
    partnum=l/k
    if l%k!=0:
        partnum+=1
    m=[""]*l
    for i in range(0,l,partnum):
        if i+partnum>=len(c):
            tmp_c=c[i:]
        else:
            tmp_c=c[i:i+partnum]
        for j in range(len(tmp_c)):
            m[j*k+i/partnum]=tmp_c[j]
    return "".join(m)
def caesar_128_encrypt(m,k):
    r=""
    for i in m:
        r+=chr((ord(i)+k)%128)
    return r
def caesar_128_decrypt(c,k):
    r=""
    for i in c:
        r+=chr((ord(i)-k)%128)
    return r
def caesar_128_brute(c,match_str):
    result=[]
    for k in range(128):
        tmp=caesar_128_decrypt(c,k)
        if match_str in tmp:
            result.append(tmp)
    return result
def caesar_128_bruteall(c):
    result=[]
    for k in range(128):
        tmp=caesar_128_decrypt(c,k)
        result.append(tmp)
    return result
def rot13(m):
    r=""
    for i in m:
        if ord(i) in range(ord('A'),ord('Z')+1):
            r+=chr((ord(i)+13-ord('A'))%26+ord('A'))
        elif ord(i) in range(ord('a'),ord('z')+1):
            r += chr((ord(i) + 13 - ord('a')) % 26 + ord('a'))
        else:
            r+=i
    return r
def caesar_alphabet_encrypt(m,k):
    r = ""
    for i in m:
        if ord(i) in range(ord('A'), ord('Z') + 1):
            r += chr((ord(i) + k - ord('A')) % 26 + ord('A'))
        elif ord(i) in range(ord('a'), ord('z') + 1):
            r += chr((ord(i) + k - ord('a')) % 26 + ord('a'))
        else:
            r += i
    return r
def caesar_alphabet_decrypt(c,k):
    r = ""
    for i in c:
        if ord(i) in range(ord('A'), ord('Z') + 1):
            r += chr((ord(i) - k - ord('A')) % 26 + ord('A'))
        elif ord(i) in range(ord('a'), ord('z') + 1):
            r += chr((ord(i) - k - ord('a')) % 26 + ord('a'))
        else:
            r += i
    return r
def caesar_alphabet_brute(c,match_str):
    result=[]
    for k in range(26):
        tmp=caesar_alphabet_decrypt(c,k)
        if match_str in tmp:
            result.append(tmp)
    return result
def caesar_alphabet_bruteall(c):
    result=[]
    for k in range(26):
        tmp=caesar_alphabet_decrypt(c,k)
        result.append(tmp)
    return result
def substitution_encode(m,k,origin="abcdefghijklmnopqrstuvwxyz"):
    r=""
    for i in m:
        if origin.find(i)!=-1:
            r+=k[origin.find(i)]
        else:
            r+=i
    return r
def substitution_decode(c,k,origin="abcdefghijklmnopqrstuvwxyz"):
    r = ""
    for i in c:
        if k.find(i) != -1:
            r += origin[k.find(i)]
        else:
            r += i
    return r
def affine_encode(m,a,b,origin="abcdefghijklmnopqrstuvwxyz"):
    r=""
    for i in m:
        if origin.find(i)!=-1:
            r+=origin[(a*origin.index(i)+b)%len(origin)]
        else:
            r+=i
    return r
def affine_decode(c,a,b,origin="abcdefghijklmnopqrstuvwxyz"):
    r=""
    n=len(origin)
    ai=primefac.modinv(a,n)%n
    for i in c:
        if origin.find(i)!=-1:
            r+=origin[(ai*(origin.index(i)-b))%len(origin)]
        else:
            r+=i
    return r
def affine_brute(c,origin="abcdefghijklmnopqrstuvwxyz"):
    result=[]
    for a in range(len(origin)):
        for b in range(len(origin)):
            result.append(affine_decode(c,a,b,origin))
    return result
def affine_guessab(m1,c1,m2,c2,origin="abcdefghijklmnopqrstuvwxyz"):
    x1=origin.index(m1)
    x2=origin.index(m2)
    y1=origin.index(c1)
    y2=origin.index(c2)
    n=len(origin)
    dxi=primefac.modinv(x1-x2,n)%n
    a=dxi*(y1-y2) % n
    b=(y1-a*x1)%n
    return (a,b)
def gen_cheese_map(k,use_Q=True,upper=True):
    k=k.upper()
    k0=""
    origin = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in k:
        if i not in k0:
            k0+=i
    for i in origin:
        if i not in k0:
            k0+=i
    if use_Q==True:
        k0=k0[0:k0.index("J")]+k0[k0.index("J")+1:]
    else:
        k0 = k0[0:k0.index("Q")] + k0[k0.index("Q") + 1:]
    if upper==False:
        k0=k0.lower()
    assert len(k0)==25
    r=[]
    for i in range(5):
        r.append(k0[i*5:i*5+5])
    return r
def playfair_encode(m,k="",cheese_map=[]):
    m=m.upper()
    origin = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    tmp=""
    for i in m:
        if i in origin:
            tmp+=i
    m=tmp
    assert k!="" or cheese_map!=[]
    if cheese_map==[]:
        map=gen_cheese_map(k)
    else:
        map=cheese_map
    m0=[]
    idx=0
    while idx<len(m):
        tmp=m[idx:idx+2]
        if tmp[0]!=tmp[1]:
            m0.append(tmp)
            idx+=2
        elif tmp[0]!="X":
            m0.append(tmp[0]+'X')
            idx+=1
        else:
            m0.append(tmp[0] + 'Q')
            idx+=1
        if idx==len(m)-1:
            if tmp[0] != "X":
                m0.append(tmp[0] + 'X')
                idx += 1
            else:
                m0.append(tmp[0] + 'Q')
                idx += 1
    r=[]
    for i in m0:
        r.append(_playfair_2char_encode(i,map))
    return r
def playfair_decode(c,k="",cheese_map=[]):
    assert k != "" or cheese_map != []
    if cheese_map == []:
        map = gen_cheese_map(k)
    else:
        map = cheese_map
    r=[]
    for i in c:
        r.append(_playfair_2char_decode(i,map))
    return "".join(r)
def polybius_encode(m,k="",name="ADFGX",cheese_map=[]):
    m=m.upper()
    assert k != "" or cheese_map != []
    if cheese_map == []:
        map = gen_cheese_map(k)
    else:
        map = cheese_map
    r=[]
    for x in m:
        for i in range(5):
            for j in range(5):
                if map[i][j]==x:
                    r.append(name[i]+name[j])
    return r
def polybius_decode(c,k="",name="ADFGX",cheese_map=[]):
    assert k != "" or cheese_map != []
    if cheese_map == []:
        map = gen_cheese_map(k)
    else:
        map = cheese_map

    r=""
    for x in c:
        i=name.index(x[0])
        j=name.index(x[1])
        r+=map[i][j]
    return r
def c01248_decode(c):
    l=c.split("0")
    origin = "abcdefghijklmnopqrstuvwxyz"
    r=""
    for i in l:
        tmp=0
        for num in i:
            tmp+=int(num)
        r+=origin[tmp-1]
    return r
def des_encrypt_ecb(m,key):
    cipher = DES.new(key, DES.MODE_ECB)
    c = cipher.encrypt(m)
    return c
def des_decrypt_ecb(c,key):
    cipher = DES.new(key, DES.MODE_ECB)
    m = cipher.encrypt(c)
    return m
def des_encrypt_cbc(m,key,iv):
    cipher = DES.new(key, DES.MODE_CBC,iv)
    c = cipher.encrypt(m)
    return c
def des_decrypt_ecb(c,key,iv):
    cipher = DES.new(key, DES.MODE_CBC,iv)
    m = cipher.encrypt(c)
    return m
def aes_encrypt_ecb(m,key):
    cipher = AES.new(key, AES.MODE_ECB)
    c = cipher.encrypt(m)
    return c
def aes_decrypt_ecb(c,key):
    cipher = AES.new(key, AES.MODE_ECB)
    m = cipher.encrypt(c)
    return m
def aes_encrypt_cbc(m,key,iv):
    cipher = AES.new(key, AES.MODE_CBC,iv)
    c = cipher.encrypt(m)
    return c
def aes_decrypt_ecb(c,key,iv):
    cipher = AES.new(key, AES.MODE_CBC,iv)
    m = cipher.encrypt(c)
    return m
def cbc_bit_attack_mul(c,m,position,target):
    l = len(position)
    r=c
    for i in range(l):
        change=position[i]-16
        tmp=chr(ord(m[position[i]])^ord(target[i])^ord(c[change]))
        r=r[0:change]+tmp+r[change+1:]
    return r
def cbc_chosen_cipher_recover_iv(cc,mm):
    assert cc[0:16]==cc[16:32]
    def _xorstr(a, b):
        s = ""
        for i in range(16):
            s += chr(ord(a[i]) ^ ord(b[i]))
        return s
    p0=mm[0:16]
    p1=mm[16:32]
    return _xorstr(_xorstr(p0, p1), cc[0:16])
def modinv(a,n):
    return primefac.modinv(a,n) % n
def gcd(a,b):
    return primefac.gcd(a,b)
def relate_message_attack(a, b, c1, c2, n):
    b3 = gmpy2.powmod(b, 3, n)
    part1 = b * (c1 + 2 * c2 - b3) % n
    part2 = a * (c1 - c2 + 2 * b3) % n
    part2 = gmpy2.invert(part2, n)
    return part1 * part2 % n
def brute_m_with_low_e(c,n,e):
    i = 0
    while 1:
        if (gmpy2.iroot(c + i * n, e)[1] == 1):
            return gmpy2.iroot(c + i * n, e)[0]
        i = i + 1
def same_n_sttack(n,e1,e2,c1,c2):
    def egcd(a, b):
        x, lastX = 0, 1
        y, lastY = 1, 0
        while (b != 0):
            q = a // b
            a, b = b, a % b
            x, lastX = lastX - q * x, x
            y, lastY = lastY - q * y, y
        return (lastX, lastY)

    s = egcd(e1, e2)
    s1 = s[0]
    s2 = s[1]
    if s1<0:
        s1 = - s1
        c1 = primefac.modinv(c1, n)
        if c1<0:
            c1+=n
    elif s2<0:
        s2 = - s2
        c2 = primefac.modinv(c2, n)
        if c2<0:
            c2+=n
    m=(pow(c1,s1,n)*pow(c2,s2,n)) % n
    return m
def broadcast_attack(data):
    def extended_gcd(a, b):
        x,y = 0, 1
        lastx, lasty = 1, 0
        while b:
            a, (q, b) = b, divmod(a,b)
            x, lastx = lastx-q*x, x
            y, lasty = lasty-q*y, y
        return (lastx, lasty, a)
    def chinese_remainder_theorem(items):
      N = 1
      for a, n in items:
        N *= n
      result = 0
      for a, n in items:
        m = N/n
        r, s, d = extended_gcd(n, m)
        if d != 1:
          N=N/n
          continue
        result += a*s*m
      return result % N, N
    x, n = chinese_remainder_theorem(data)
    m = gmpy2.iroot(x, 3)[0]
    return m
