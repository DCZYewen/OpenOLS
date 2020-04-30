from fastapi import FastAPI
import base64
from Crypto.Cipher import AES
import psycopg2
import sys
import string
import time
import site_settings
import random
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from fastapi.middleware.cors import CORSMiddleware
import Lib.supervise

#All constants declaration
tz = 8 #声明时区UTC+8
site_url = site_settings.site_url
api_url = site_settings.api_url
aes_key = site_settings.aes_key
html = site_settings.html
hash_hey = site_settings.hash_key

#program startups
app = FastAPI()
conn = psycopg2.connect(database="TEST1", user="postgres", password="dachengzi", host="10.0.10.102", port="5432") #password in this line is invalid 
cur = conn.cursor()
cur.execute('SELECT * FROM TOKENS ORDER BY TOKEN_NO DESC LIMIT 1;')
global TOKEN_NO
TOKEN_NO = cur.fetchone()#声明全局变量
TOKEN_NO = TOKEN_NO[0]#你可能会笑我 但是我就这么写了
percent = Lib.supervise.percent
per_percent = Lib.supervise.per_percent
logical = Lib.supervise.logical_count
cpus = Lib.supervise.cpu_count
total = Lib.supervise.mem.total
free = Lib.supervise.mem.free

#接入CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:6000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")#This is for main page
async def root():
    return(html)

@app.get("/status")#this is for heartbeat to detect the client status
async def status_check(user_id: int, time_stamp: int ,status: bool):#接收状态信息
    return("status" , "OK")

@app.get("/ping")#this is for getting the ping of the server 
async def root():
    return("status" , "OK")

@app.get("/login/")
async def read_item(username: str , password: str, time: str): #这里是登录API,主要实现功能是客户端点击login将get http://site.com/login/?username=2&password=2&time=200303031211
    user_information = {"username": username,"password": password,"time":str}
    #进入登录验证部分
    real_pass = get_real_pass(password,time)
    init = "ACCOUNT = '" + username + "'"
    result = SELECT_FUNC('USERS',init)
    if not result == None: #登陆逻辑判断建议隐藏了因为我也不想看这一堆玩意
        if check_password_hash(result[5],real_pass):
            if result[6]=='ADMIN':
                login_admin_item = {"status" : "OK",
                "redirect_url" : site_url + '/Admin',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[6]),
                "tab" : 0
                }
                print(login_admin_item)
                return login_admin_item
            elif result[6]=='STUDENT':
                login_stu_item = {"status" : "OK",
                "redirect_url" : site_url + '/MainPage',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[6]),
                "tab" : 0
                }
                print(login_stu_item)
                return login_stu_item
            elif result[6]=='TEACHER':
                login_teacher_item = {"status" : "OK",
                "redirect_url" : site_url + '/Teacher',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[6]),
                "tab" : 0
                }
                print(login_teacher_item)
                return login_teacher_item
            else:
                pass
        else:
            return "AUTH_ERROR"
    else:
        return "AUTH_ERROR_NOUSER"

@app.get("/get_new_token")#刷新token用
async def flush(user_id: int , token: str):
    user_id = str(user_id)
    token = token.replace(' ','+')
    print(token)
    new_token = token_create(user_id,True,token)
    if new_token[1] == 'token_authentication_failure':
        return ("status","token_authentication_failure")
    else :
        back_item = {"status":"ok",
        "user_id" : user_id,
        "token" : new_token
        }#构造返回结构
        return back_item

@app.get("/logout")#销毁Token，登出
async def logout(user_id: int , token: str):
    init = "TOKEN = '" + token + "'"
    user_id = str(user_id)
    TOKEN_ITEM = SELECT_FUNC('tokens',init)
    check_item = token_check(token)
    if TOKEN_ITEM==None :
        return("status" , "logout_failed")
    elif not check_item == 'TOKEN VALID':
        return("status" , "OK")
    elif check_item == 'TOKEN VALID':
        init = "EXPIRED = True WHERE USER_ID = " + user_id
        UPDATA_FUNC('tokens',init)
        return("status","OK")
    else :
        return("status" , "logout_failed")
    pass

@app.get("/mainpage")#这个API默认了user_id存在，后续可能会增加进一步的错误处理
async def mainpage(token: str , user_id: int ):
    init = "TOKEN = '" + token + "'"
    user_id = str(user_id)
    TOKEN_ITEM = SELECT_FUNC('tokens',init)
    init = "USER_ID = '" + user_id + "'"
    USER_ITEM = SELECT_FUNC('USERS',init)
    check_item = auth_func(user_id,token)
    return_item = {
        "status" : "OK",
        'statistics' : {
            "CPUS" : logical,
            "Total_Usage" : percent,
            "Per_Usage" : per_percent,
            "Total_Mem" : total ,
            "Free_Mem" : free 
        },
        'information' : {
            'name' : USER_ITEM[1],
            'grade' : USER_ITEM[2],
            'auth' : USER_ITEM[6],
            'last_course': USER_ITEM[8],
            'exit_time' : USER_ITEM[9],
            'gender' : USER_ITEM[10],
            'intro' : USER_ITEM[11],
            'motto' : USER_ITEM[12]
        }
        
    }
    if not check_item == 'TOKEN VALID':
        return("status","AUTH_ERROR")
    else :
        return return_item
    pass

##获取前端弱鸡加密过的密码
def get_real_pass(password,time):
    encoder = base64.b64decode(password.encode('utf-8'))
    decode_string = encoder.decode('utf-8')
    i = len(decode_string)
    if int(time) < 10 :
        real_pass = decode_string[1:i-1]
    else :
        real_pass = decode_string[2:i-2]
    return str(real_pass)

##插库驱动函数（单行
def INSERT_FUNC(table,*args):
    TURPLE_COUNTER = 0
    sql = 'INSERT INTO ' + str(table) + " VALUES ('"#构造SQL语句
    while len(args) > TURPLE_COUNTER + 1:
        sql = sql + str(args[TURPLE_COUNTER]) + "', '"
        TURPLE_COUNTER = TURPLE_COUNTER + 1
    
    sql = sql + str(args[TURPLE_COUNTER]) + "');"
    print(sql)
    cur.execute(sql)
    conn.commit()

##查库驱动函数（单字段 单条件 单返回结果
def SELECT_FUNC(table,operators):
    sql = "SELECT * FROM " + str(table) + " WHERE " + operators
    cur.execute(sql)
    return cur.fetchone()

##更新数据库的驱动函数（单字段
def UPDATA_FUNC(table,operators):
    sql = "UPDATE " + str(table) + " SET " + operators
    cur.execute(sql)
    print("Something UPDATED")

#创建一个token 并初始化信息 同时，当上一个token存在的时候，将上一个token过期
#这里我使用了一个Flag表示函数是否由登陆函数调起，因为登陆时不会传入上一个token 即 如果第二个参数是False表示其由登陆函数拉起
def token_create(user_id,*args):
    OUT_FLAG = False
    global TOKEN_NO
    time = get_time_string() + '00'
    user_id = str(user_id)
    TOKEN_STRING = user_id + time
    encrypted = encrypt_oracle(aes_key,TOKEN_STRING)
    init = "USER_ID = '" + user_id + "'" #此处获取user的权限
    AUTH = SELECT_FUNC('users',init)
    if AUTH:
        AUTH = AUTH[7]
    else :
        pass

    if args[0] == True:#程序的这个分支保证token不会被恶意过期
        check_item = token_check(args[1])
        print(check_item)
        if check_item == 'ERROR TOKEN NOT EXIST' or check_item == 'TOKEN EXPIRED' or check_item == 'TOKEN TIME INVAID' :#如果传入的token并不存在或者已过期
            return ("info" , "token_authentication_failure")
        else :#如果传入的token和user_id对应
            sql = "SELECT * FROM TOKENS WHERE USER_ID = '" + user_id + "'" + " ORDER BY TOKEN_NO DESC LIMIT 1 "
            cur.execute(sql)
            token_user = cur.fetchone()
            if token_user[3] == args[1]:
                init = "EXPIRED = True WHERE USER_ID = " + user_id
                UPDATA_FUNC('tokens',init)
            else :
                AUTH = None
    else :
        init = "USER_ID = '" + user_id + "'"
        TOKEN_ITEM = SELECT_FUNC('TOKENS',init)
        if TOKEN_ITEM == None :#如果该用户上一个TOKEN不存在
            pass
        else :#当上一个token存在的时候expire它
            init = "EXPIRED = True WHERE USER_ID = " + user_id
            UPDATA_FUNC('tokens',init)#这里强制过期上一个token
    if AUTH == None:
        return ("info" , "token_authentication_failure")
    else :
        INSERT_FUNC('tokens',TOKEN_NO + 1,time,'False',encrypted,user_id,AUTH)
        TOKEN_NO = TOKEN_NO + 1 #注意这里将初始化时的TOKEN_NO加一，表示添加了一条记录
        return encrypted

def token_check(token):#检查token有效性无非3样，token不存在，键值记录的token确已过期，token时间已经过期，如果三种验证都pass了，token就有效
    init = "TOKEN = '" + token + "'"
    TOKEN_ITEM = SELECT_FUNC('TOKENS',init)
    if TOKEN_ITEM == None :#如果token不存在，抛出异常
        return 'ERROR TOKEN NOT EXIST'
    elif TOKEN_ITEM[2] == True :
        return 'TOKEN EXPIRED'
    elif token_is_valid(TOKEN_ITEM[1][:14]):#最复杂的部分，由于数据库时间为16位
        return 'TOKEN TIME INVAID'
    else :
        return 'TOKEN VALID'


#This is for AES password encryption and decryption
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

def encrypt_oracle(key,password):
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(password))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    encrypted_text = encrypted_text[0:len(encrypted_text) - 1]
    return encrypted_text

def decrypt_oracle(key,encrypted_text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(encrypted_text.encode(encoding='utf-8'))
    #执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','') 
    return(decrypted_text)

def get_time_string():#这是一个获取当前时间字符串格式的函数（精确到秒
    localtime = time.localtime(time.time())
    time_entity = time.strftime("%Y%m%d%H%M%S",localtime)
    return time_entity

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

def auth_func(user_id,token):#不打算更改已经写的代码了，这里抄一份改改
    init = "TOKEN = '" + token + "'"
    user_id = str(user_id)
    TOKEN_ITEM = SELECT_FUNC('TOKENS',init)
    if TOKEN_ITEM == None :#如果token不存在，抛出异常
        return 'ERROR TOKEN NOT EXIST'
    elif TOKEN_ITEM[2] == True :
        return 'TOKEN EXPIRED'
    elif token_is_valid(TOKEN_ITEM[1][:14]):#最复杂的部分，由于数据库时间为16位
        return 'TOKEN TIME INVAID'
    elif not TOKEN_ITEM[3] == user_id:
        return 'ID TOKEN NOT MATCH'
    else :
        return 'TOKEN VALID'
    pass