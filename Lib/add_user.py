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

#ADD SUPER USER
sql1 = "\
    INSERT INTO USERS VALUES(\
        99999999 , 'Administrator' , 2099 , 99 , 99999999 , "  + "'" + generate_password_hash('admin') + "'" + ''' , 'ADMIN' , 'admin' , 000000 , '2002020202020200' , '男' , '无' , '无' 
    )
'''

#ADD STU
sql = "\
    INSERT INTO USERS VALUES(\
        99999998 , 'Test_Stu1' , 2099 , 99 , 99999998 , "  + "'" + generate_password_hash('student1') + "'" + ''' , 'STUDENT' , 'student1' , 000000 , '2002020202020200' , '男' , '心有猛虎，轻嗅蔷薇。' , '这个男人简直失了智。' 
    )
'''

#ADD TEACHER
sql2 = "\
    INSERT INTO USERS VALUES(\
        99999997 , 'TEACHER1' , 2099 , 99 , 99999997 , "  + "'" + generate_password_hash('teacher1') + "'" + ''' ,'TEACHER' , 'teacher1' , 000000 , '2002020202020200' , '男' , '无' , '无' 
    )
'''

#USER_ID| NAME  | GRADE | CLASS   | CHAT_ID | PASSWD | IS_ONLNE | AUTH | ACCOUNT
cur.execute(sql1)
cur.execute(sql)
cur.execute(sql2)
conn.commit()
print("User Created , super account admin super password admin .\n Test Teacher : Teast_Teacher1 teacher1 \n Test Student Test_Stu1 student1")
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