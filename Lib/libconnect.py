import psycopg2

conn = psycopg2.connect(database="test1", user="postgres", password="dachengzi", host="127.0.0.1", port="5432") #password in this line is invalid 
cur = conn.cursor()