import sys
import psycopg2

conn = psycopg2.connect(database="TEST1", user="postgres", password="dachengzi", host="10.0.10.102", port="5432") #password in this line is invalid 
cur = conn.cursor()

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
        TIME_START  TEXT           NOT NULL,\
        TIME_END    TEXT           NOT NULL)")
print("Table COURSE created successfully")
#|COURSE_ID| TITLE           | PEOPLE |VISIBILITY |LISTENING |TIME_START      |TIME_END        |

cur.execute("CREATE TABLE LOCATIONS\
            (COURSE_ID INT PRIMARY KEY NOT NULL,\
            RTMP_URL  TEXT            NOT NULL,\
            CHAT_URL  TEXT            NOT NULL,\
            BOARD_URL TEXT            NOT NULL)")
#|CLASS_ID| RTMP_URL     |CHAT_URL     | BOARD_URL            | 
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


print("Database successfully initiallized")
conn.commit()
conn.close()