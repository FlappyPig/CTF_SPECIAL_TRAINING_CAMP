#whitehat-grand-prix-qualification-2015
import base64
s1 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
s2 = 'ELF8n0BKxOCbj/WU9mwle4cG6hytqD+P3kZ7AzYsag2NufopRSIVQHMXJri51Tdv'
dict = {}
for i in range(len(s1)):
    dict[s2[i]] = s1[i]
dict['='] = '='

output = 'ms4otszPhcr7tMmzGMkHyFn='
s3 = ''
for i in range(len(output)):
    s3 += dict[output[i]]
flag = base64.b64decode(s3)
print flag
#Funny_encode_huh!
