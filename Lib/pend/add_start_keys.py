import psycopg2


conn = psycopg2.connect(database="test1", user="postgres", password="dachengzi", host="127.0.0.1", port="5432") #password in this line is invalid 
cur = conn.cursor()

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
conn.close()
