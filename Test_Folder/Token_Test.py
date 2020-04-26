import time
def fmt_time(time_string): #返回时间元组和时间戳
    stamp = str(time.mktime(time.strptime(time_string,"%Y%m%d%H%M%S")))
    return stamp

def token_is_valid(token_create_time):#检查TOKEN是否已经过时的函数
    ts1 = fmt_time(token_create_time)
    #print(str(ts1))
    ts2 = fmt_time(get_time_string())
    #print(str(ts2))
    if 0 < float(ts1) - float(ts2) < 3600 :
        return True
    else :
        return False

def get_time_string():#这是一个获取当前时间字符串格式的函数（精确到秒
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
    return time_entity

print(token_is_valid('20200426180000'))