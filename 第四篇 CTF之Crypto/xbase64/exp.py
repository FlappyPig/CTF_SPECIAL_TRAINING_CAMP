new_base64_table = ['=','A', 'B', 'C', 'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                'a', 'b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                '0', '1', '2', '3','4','5','6','7','8','9',
                '+', '/'][::-1]
old_base64_table = ['A', 'B', 'C', 'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                'a', 'b', 'c', 'd','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
                '0', '1', '2', '3','4','5','6','7','8','9',
                '+', '/','=']
target="mZOemISXmpOTkKCHkp6Rgv=="
s=""
for i in target:
    s+=old_base64_table[new_base64_table.index(i)]
print s.decode("base64")