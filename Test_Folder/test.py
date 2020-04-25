import time
localtime = time.localtime(time.time())

if localtime[1] <= 10:
    mon = '0' + str(localtime[1])
else:
    mon = str(localtime[1])

if localtime[2] <= 10:
    day = '0' + str(localtime[2])
else:
    day = str(localtime[2])

if localtime[3] <= 10:
    day = '0' + str(localtime[3])
else:
    day = str(localtime[3])

if localtime[1] <= 10:
    day = '0' + str(localtime[2])
else:
    day = str(localtime[2])
print(localtime)
print(mon)
print(localtime[2])