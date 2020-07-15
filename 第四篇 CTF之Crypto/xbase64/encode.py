# /usr/bin/python
# encoding: utf-8
base64_table = ['=','A', 'B', 'C', 'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                'a', 'b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                '0', '1', '2', '3','4','5','6','7','8','9',
                '+', '/'][::-1]

def encode_b64(s):
    l = len(s)
    i = 0
    result = ''
    while i < l:
        # 将字符转换为二进制编码，然后对齐
        s1 = s[i]
        b1 = bin(ord(s1))[2:]
        cb1 = b1.rjust(8, '0')

        i += 1
        if i >= l:
            cb2 = '00000000'
        else:
            s2 = s[i]
            b2 = bin(ord(s2))[2:]
            cb2 = b2.rjust(8, '0')

        i += 1
        if i >= l:
            cb3 = '00000000'
        else:
            s3 = s[i]
            b3 = bin(ord(s3))[2:]
            cb3 = b3.rjust(8, '0')

        # 将三字节转换为四字节
        cb = cb1 + cb2 + cb3

        rb1 = cb[:6]
        rb2 = cb[6:12]
        rb3 = cb[12:18]
        rb4 = cb[18:]

        # 转换后的编码转为十进制备用
        ri1 = int(rb1, 2)
        ri2 = int(rb2, 2)
        ri3 = int(rb3, 2)
        ri4 = int(rb4, 2)

        # 处理末尾为０的情况，以＇＝＇填充
        if i - 1 >= l and ri3 == 0:
            ri3 = -1

        if i >= l and ri4 == 0:
            ri4 = -1

        result += base64_table[ri1] + base64_table[ri2] + base64_table[ri3] + base64_table[ri4]

        i += 1

    return result

print encode_b64(open("flag","r").read())

#output: mZOemISXmpOTkKCHkp6Rgv==