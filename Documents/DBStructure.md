
## Data Structure

---------------------------------


For Table Users

| USER_ID| NAME  | GRADE | CLASS_ID| CHAT_ID | PASSWD | AUTH   | ACCOUNT|LAST_COURSE|EXIT_TIME     |GENDER |INTRO    |MOTTO    |
| ------- | ---- | ----- | ------- | ------- | -----  | ------ | ------ | -------- | ------------ | ----- | ------- | -------- |
|90155664|吴此仁  | 2018  | 201815  |885823  |17ac5be | STUDENT| 114514 |00000001   |20200418220000|男     |并不存在的|并无格言  |



---------------------------------

For Table Course


|COURSE_ID| TITLE       | PEOPLE | VISIBILITY |LISTENING|TIME_START      |TIME_END        |IS_END    | TEACHER_ID |
| ------- | ----------- | ------ | ---------- | ------- | ------------- | -------------- | --------  |  --------  |
|00000001 | 不存在的网课 | 45     | 1\s2\s3\s  |25       |20200405205735  |20200405220000  |True      |  99999994  |


---------------------------------

For Table Locations

|COURSE_ID| LIVE_URL            |CHAT_URL     | RECORD_URL           | 
|---------|---------------------|-------------|----------------------|
|00000001 | https://a.com/a.flv | ws://a.com/1| https://a.com/a.flv  |

---------------------------------

For Table Resources

|RESOURCE_ID |TYPE   |FILE_NAME|URL                          |VISIBILITY |FILE_OWNER|OWNER_ID|INTRO   |UPLOAD_TIME   |COVER_URL         |SIZE       |
|------------|-------|---------|-----------------------------|-----------|----------|--------|--------|--------------|------------------|-----------|
|000000000001|MP4    |TokyoCold|https://a.com/tokyocold.mp4  |1\s2\s\14\s|Teacher1  |99999997|A video |20200429171400|http://a.com/a.jpg|13550014   |

---------------------------------

For Table Tokens

|Token_NO| Time_CREATED | EXPIRED | TOKEN     | USER_ID  |AUTH |
|--------|--------------|---------|-----------|----------|-----|
|0000001 |20200418220000| False   | 39e9e146c9| 90155664 |admin|

---------------------------------

For Table LiveLog

|COURSE_ID| USER_ID  |EVENT  |TIME           |
|---------|----------| ----- | ------------- |
|0000001  | 90155664 |OnClose|20200705205735 |

---------------------------------

For Table Useractivity

| USER_ID  | TIME           | EVENT     | ID        |  TYPE  |
|----------| -------------- | --------- | --------- | ------ |
| 90155664 | 20200705205735 | PLAY      | 12364576  | LIVE   |

---------------------------------


