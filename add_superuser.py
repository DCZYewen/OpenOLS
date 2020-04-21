import psycopg2
import sys
import random
import string
import site_settings
import base64
from Crypto.Cipher import AES
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


conn = psycopg2.connect(database="TEST1", user="postgres", password="dachengzi", host="10.0.10.102", port="5432") #password in this line is invalid 
cur = conn.cursor()

#encrypt the default pass
aes_key = site_settings.aes_key
hash_hey = site_settings.hash_key


sql = "\
    INSERT INTO USERS VALUES(\
        99999999 , 'Administrator' , 2099 , 99 , 99999999 , "  + "'" + generate_password_hash('admin') + "'" + ''' , false , 'ADMIN' , 'admin'
    )
'''


cur.execute(sql)
#USER_ID| NAME  | GRADE | CLASS   | CHAT_ID | PASSWD | IS_ONLNE | AUTH | ACCOUNT
conn.commit()
print("Super User Created , super account admin super password admin , Please CHANGE your password in the site .")
conn.close()


##加密AES
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
    return encrypted_text