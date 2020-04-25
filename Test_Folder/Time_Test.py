import time
localtime = time.localtime(time.time())

if localtime[1] <= 10:#格式化月份
    mon = '0' + str(localtime[1])
else:
    mon = str(localtime[1])

if localtime[2] <= 10:#天
    day = '0' + str(localtime[2])
else:
    day = str(localtime[2])

if localtime[3] <= 10:#小时
    hour = '0' + str(localtime[3])
else:
    hour = str(localtime[3])

if localtime[4] <= 10:#分钟
    min = '0' + str(localtime[4])
else:
    min = str(localtime[4])

if localtime[5] <= 10:#秒
    sec = '0' + str(localtime[5])
else:
    sec = str(localtime[5])

time_entity = str(localtime[0])+mon+day+hour+min+sec
MAIN_LOOP_COUNTER = 0
print(time_entity[MAIN_LOOP_COUNTER : len(time_entity) - MAIN_LOOP_COUNTER])
print(time_entity)