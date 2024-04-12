import time
from datetime import datetime
import json

current_datetime = datetime.now()
current_time = time.time()

lst = []
for x in range(1,1000000) :
    print(x)
    for y in range (1,1000000) :
        result = x*y
        number = result % 27
        if number == 0 :
            lst.append(result)

outFile = open('garbage.txt', 'w')
outFile.write(f'{json.dumps(lst)}\n\n\nLIST LENGTH: {len(lst)}\n\n\nTIME TAKEN: {time.time()-current_time}')
outFile.close()

print (lst)
print(f'time taken: {datetime.now()-current_datetime} seconds')