left = 0x2724090c0798e4c5 
mi = 13337  
mo = 64  
right = []  
  
for i in range(mo):  
    m = (pow(2, i + 1))  
    l = left % m  
    r = 0  
    for index, value in enumerate(right):  
        r += value * pow(2, index)  
    if pow(r, mi, m) == l:  
        right.append(0)  
    elif pow((r + pow(2, i)), mi, m) == l:  
        right.append(1)  
    else:  
        raise  
r = 0  
for index, value in enumerate(right):  
    r += value * pow(2, index)  
print r 
