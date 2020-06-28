import libconnect
import sys
import random
import string
import base64

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

conn = libconnect.conn
cur = libconnect.cur

cur.execute('''CREATE TABLE USERS (USER_ID        INT     NOT NULL,
NAME           TEXT    NOT NULL,
GRADE          INT     NOT NULL,
CLASS_ID       INT     NOT NULL,
CHAT_ID        INT     NOT NULL,
PASSWD         TEXT    NOT NULL,
AUTH           TEXT    NOT NULL,
ACCOUNT        TEXT    NOT NULL,
LAST_COURSE    TEXT,
EXIT_TIME      TEXT,
GENDER         TEXT     NOT NULL,
INTRO          TEXT    NOT NULL,
MOTTO          TEXT    NOT NULL,
PRIMARY KEY(USER_ID));''')
print("Table USERS created successfully")
#USER_ID| NAME  | GRADE | CLASS   | CHAT_ID | PASSWD | AUTH | ACCOUNT | LAST_COURSE|EXIT_TIME     |GENDER |INTRO    |MOTTO    |

cur.execute("CREATE TABLE COURSE\
        (COURSE_ID  INT PRIMARY KEY NOT NULL,\
        TITLE       TEXT            NOT NULL,\
        PEOPLE      INT             NOT NULL,\
        VISIBILITY  TEXT            NOT NULL,\
        LISTENING   INT             NOT NULL,\
        TIME_START  TEXT            NOT NULL,\
        TIME_END    TEXT            NOT NULL,\
        IS_END      BOOLEAN         NOT NULL)")
print("Table COURSE created successfully")
#|COURSE_ID| TITLE           | PEOPLE |VISIBILITY |LISTENING |TIME_START   |TIME_END    | IS_END|

cur.execute("CREATE TABLE LOCATIONS\
            (COURSE_ID INT PRIMARY KEY NOT NULL,\
            RTMP_URL  TEXT            NOT NULL,\
            CHAT_URL  TEXT            NOT NULL,\
            BOARD_URL TEXT            NOT NULL)")
#|CLASS_ID| RTMP_URL    |CHAT_URL    | BOARD_URL   | 
print("Table LOCATIONS created successfully")

cur.execute("CREATE TABLE RESOURCES\
            (RESOURCE_ID INT PRIMARY KEY NOT NULL,\
            TYPE         TEXT            NOT NULL,\
            FILE_NAME    TEXT            NOT NULL,\
            URL          TEXT            NOT NULL,\
            VISIBILITY   TEXT            NOT NULL,\
            FILE_OWNER   TEXT            NOT NULL,\
            OWNER_ID     INT             NOT NULL,\
            INTRO        TEXT            NOT NULL,\
            UPLOAD_TIME  TEXT            NOT NULL,\
            COVER_URL    TEXT            NOT NULL,\
            SIZE         INT             NOT NULL)")
print("Table RESOURCES created successfully")
#|RESOURCE_ID |TYPE |FILE_NAME|URL |VISIBILITY |FILE_OWNER|OWNER_ID|INTRO  |UPLOAD_TIME   |COVER_URL    |SIZE |

cur.execute("CREATE TABLE TOKENS\
            (TOKEN_NO    INT PRIMARY KEY NOT NULL,\
            TIME_CREATED TEXT       NOT NULL,\
            EXPIRED      BOOLEAN         NOT NULL,\
            TOKEN        TEXT            NOT NULL,\
            USER_ID      INT             NOT NULL,\
            AUTH         TEXT            NOT NULL)")
print("Table TOKENS created successfully")
#|0000001 |20200418220000| False   | 39e9e146c9| 90155664| admin |

conn.commit()

print("Database successfully initiallized")


sql = "\
    INSERT INTO TOKENS VALUES(\
        00000001 , '20200418220000' , False , '39e9e146c9' , 99999998 , 'admin')"
cur.execute(sql)

sql = "\
    INSERT INTO COURSE VALUES(\
        00000001 , '一个不存在的网课' , 42 , '1/s23/s' , 23 , '2002022312124500' , '2020022312124500', False)"
cur.execute(sql)

conn.commit()
print("Initial key successfully inserted ! ")

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