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
            if result[7]=='ADMIN':
                login_admin_item = {"status" : "OK",
                "redirect_url" : site_url + '/Admin',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[7]),
                "tab" : 0
                }
                print(login_admin_item)
                return login_admin_item
            elif result[7]=='STUDENT':
                login_stu_item = {"status" : "OK",
                "redirect_url" : site_url + '/MainPage',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[7]),
                "tab" : 0
                }
                print(login_stu_item)
                return login_stu_item
            elif result[7]=='TEACHER':
                login_teacher_item = {"status" : "OK",
                "redirect_url" : site_url + '/Teacher',
                "user_id" : result[0],
                "token" : token_create(result[0],False),
                "AUTH" : str.upper(result[7]),
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
    new_token = token_create(user_id,True,token)
    if new_token[1] == 'token_authentication_failure':
        return ("status","token_authentication_failure")
    else :
        back_item = {"status":"ok",
        "user_id" : user_id,
        "token" : new_token
        }#构造返回结构
        return back_item



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
    AUTH = SELECT_FUNC('users',init)[7]

    if args[0] == True:#程序的这个分支保证token不会被恶意过期
        init = "TOKEN = '" + str(args[1]) + "'"
        TOKEN_ITEM = SELECT_FUNC('TOKENS',init)
        print(TOKEN_ITEM)
        if TOKEN_ITEM == None or TOKEN_ITEM[2] == True:#如果传入的token并不存在或者已过期
            return ("info" , "token_authentication_failure")
        else :#如果传入的token和user_id对应
            init = "EXPIRED = True WHERE USER_ID = " + user_id
            UPDATA_FUNC('tokens',init)
    else :
        init = "USER_ID = '" + user_id + "'"
        TOKEN_ITEM = SELECT_FUNC('TOKENS',init)
        if TOKEN_ITEM == None :#如果该用户上一个TOKEN不存在
            pass
        else :#当上一个token存在的时候expire它
            init = "EXPIRED = True WHERE USER_ID = " + user_id
            UPDATA_FUNC('tokens',init)#这里强制过期上一个token

    INSERT_FUNC('tokens',TOKEN_NO + 1,time,'False',encrypted,user_id,AUTH)
    TOKEN_NO = TOKEN_NO + 1 #注意这里将初始化时的TOKEN_NO加一，表示添加了一条记录
    return encrypted

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