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
print(time_entity)
def divide_time(time):#传入我们定义的time_string，获取各个时间量
    time = time[0][0:11]#这里反向构造出时间的变量
    yr = time[0:3]
    mon = time[4:5]
    day = time[6:7]
    hour = time[8:9]
    min = time[10:11]
    return [yr,mon,day,hour,min]

def compare(time1,time2):#如果时间1比时间2大就返回True
    #比较年份
    if time1[0] > time2[0]:
        #比较月份
        if time1[1] > time2[1] :
            #比较天数
            if time1[2] > time2[2] :
                #比较小时#比较分钟
                if time1[3] > time2[3]:
                    

time1 = '202004260620010'
time2 = time_entity
if compare(divide_time(time1),divide_time(time2)):
    print("OK")
elif compare(divide_time(time2),divide_time(time1)):
    print("OK2")
else :
    print("OK3")