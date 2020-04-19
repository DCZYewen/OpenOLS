import sys
import psycopg2

conn = psycopg2.connect(database="TEST1", user="postgres", password="dachengzi", host="10.0.10.102", port="5432") #password in this line is invalid 
cur = conn.cursor()

cur.execute('''CREATE TABLE USERS (USER_ID        INT     NOT NULL,
NAME           TEXT    NOT NULL,
GRADE          INT     NOT NULL,
CLASS          INT     NOT NULL,
CHAT_ID        INT     NOT NULL,
PASSWD         TEXT    NOT NULL,
IS_ONLINE      BOOLEAN NOT NULL,
AUTH           TEXT    NOT NULL,
ACCOUNT        TEXT    NOT NULL,
PRIMARY KEY(USER_ID));''')
print("Table USERS created successfully")
#USER_ID| NAME  | GRADE | CLASS   | CHAT_ID | PASSWD | IS_ONLNE | AUTH | ACCOUNT

cur.execute("CREATE TABLE COURSE\
        (COURSE_ID INT PRIMARY KEY NOT NULL,\
        TITLE     TEXT            NOT NULL,\
        PEOPLE    INT             NOT NULL,\
        CLASS_IN  TEXT            NOT NULL,\
        LISTENING INT             NOT NULL,\
        TIME_START TIMESTAMP      NOT NULL,\
        TIME_END   TIMESTAMP     NOT NULL)")
print("Table COURSE created successfully")
#|COURSE_ID| TITLE           | PEOPLE | CLASS_IN   |LISTENING| PASSWD |TIME_START      |TIME_END        |

cur.execute("CREATE TABLE URLS\
            (COURSE_ID INT PRIMARY KEY NOT NULL,\
            RTMP_URL  TEXT            NOT NULL,\
            CHAT_URL  TEXT            NOT NULL,\
            BOARD_URL TEXT            NOT NULL)")
#|CLASS_ID| RTMP_URL     |CHAT_URL     | BOARD_URL            | 
print("Table URLS created successfully")

cur.execute("CREATE TABLE CLASSES\
            (CLASS_ID INT PRIMARY KEY NOT NULL,\
            GRADE    INT             NOT NULL,\
            CLASS    INT             NOT NULL,\
            MEMBERS  INT             NOT NULL)")
print("Table CLASSES created successfully")
#|201815  |2018  | 15    | 45      |

cur.execute("CREATE TABLE TOKENS\
            (TOKEN_NO    INT PRIMARY KEY NOT NULL,\
            TIME_CREATED TIMESTAMP       NOT NULL,\
            EXPIRED      BOOLEAN         NOT NULL,\
            TOKEN        TEXT            NOT NULL)")
print("Table TOKENS created successfully")
#|0000001 |20200418220000| False   | 39e9e146c9|


print("Database successfully initiallized")
conn.commit()
conn.close()