import libconnect

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

conn = libconnect.conn
cur = libconnect.cur

##本库主要为OpenOLS编写，封装了常用的增删改查方法
##只能在单个表内操作




#增增增增增增增增增增增增增增增增增增增增增增增增
def insertFulline(table,InsertLine):#提供全行数据的插入
##insertFulline(USERS,makeInsertLine('1','2','3'))
    sql = 'INSERT INTO ' + table + ' VALUES (' + InsertLine + ');'
    if not securitySQL(sql) :
        cur.execute(sql)
        conn.commit()
    else :
        return "FUCK I M UNSDER ATTACK"

## Test Pass ! Thanks to the mercy of pgsql !

def insertByRow():#插入在指定的列里（应该没有乱用
##insertByRow(USERS,makeInsertCol(user_id,name,somewhat),makeInsertLine('1','2','3'))
##由于OpenOLS从关系上限制任何键值不能为空，所以这个函数应该是没有卵用，但还是实现了
    pass




#删删删删删删删删删删删删删删删删删删删删删删删删
def deleteByID(table , id , id_form):#以ID为索引删除一行,id_form是id的具体描述，比如user_id，class_id等等
##deleteByID(USERS,114514,user_id)
    sql = 'DELETE FROM ' + table + ' WHERE ' + id_form + '=' + str(id) + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        conn.commit()
    else :
        return "FUCK I M UNSDER ATTACK"
## Test Pass ! Thanks to the mercy of pgsql !



def deleteByIndex(table,key_word,value):#删除给定一个删除的索引
##deleteByIndex(USERS,'class',13)把13班的用户都删除
    sql = 'DELETE FROM ' + table + ' WHERE ' + key_word + '=' + str(value) + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        conn.commit()
    else :
        return "FUCK I M UNSDER ATTACK"
#说实话我觉得这玩意没个鸡儿用，但是还是写了，为了逼格



#改改改改改改改改改改改改改改改改改改改改改改改改
def updateByID(table,UpdateLine,id,id_form):#以ID为索引修改
##updateByID(USERS,makeUpdateLine('class',13,'gender','male'),114514,user_id)把ID为114514的人的class属性改成13，性别改成male
    sql = 'UPDATE ' + table + ' SET ' + UpdateLine + ' WHERE ' + str(id) + '=' + id_form + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        conn.commit()
    else :
        return "FUCK I M UNSDER ATTACK"
## Test Pass ! Thanks to the mercy of pgsql !

def updateByIndex(table,UpdateLine,key_word,value):#索引指定的索引更改
##deleteByIndex(USERS,makeUpdateLine('class',13,'gender','male'),auth,admin)把auth为admin的人的class属性改成13，性别改成male
    sql = 'UPDATE ' + table + ' SET ' + UpdateLine + ' WHERE ' + key_word + '=' + str(value) + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        conn.commit()
    else :
        return "FUCK I M UNSDER ATTACK"

#查查查查查查查查查查查查查查查查查查查查查查查查
## Tips，查找结果一律按ID排序

def selectAll(table):#只有当生成统计信息时使用，不要调用！
    sql = 'SELECT * FROM ' + table + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        return(cur.fetchall())
    else :
        return "FUCK I M UNSDER ATTACK"
## Test Pass ! Thanks to the mercy of pgsql !

def selectByID(table , SelectLine , id , id_form):#根据ID获取一整行数据
##selectByID(USERS,makeSelectLine(user_id,auth),114514,user_id)把114514的ID的userid和auth选取出来
##这个函数大概率会用在展示用户列表上
    sql = 'SELECT ' + SelectLine + ' FROM ' + table + ' WHERE ' + id_form + '=' + str(id) + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        return(cur.fetchone())
    else :
        return "FUCK I M UNSDER ATTACK"
## Test Pass ! Thanks to the mercy of pgsql !

def selectByIndex(table , SelectIndex ):#根据给定的索引选取一整行数据
##selectByIndex(USERS,makeSelectIndex(user_id,114514))这个和上一个函数的实例should do the same 
    sql = 'SELECT ' + SelectIndex + ' FROM ' + table + ';'
    if not securitySQL(sql) :
        cur.execute(sql)
        return(cur.fetchall())
    else :
        return "FUCK I M UNSDER ATTACK"


def findByValue():#查找一个值
##findByValue():##估计没个鸡儿用，爷懒得写了
##抄一段SQL吧SELECT * FROM Persons WHERE City='Beijing';
    pass




#辅助构造数据结构
def makeInsertLine(*args):
    string = "'"
    for temp in args:
        string = string + str(temp) + "','"
    string = string[0:len(string)-2]
    return string##返回类似i,am,a,sb的字符串

def makeInsertCol():
    pass

def makeUpdateLine(*args):
    tmpList = []
    Jmp_Flag = False

    for tmp in args:
        tmpList.append(tmp)

    string = ''
    for tmp in tmpList:
        if not Jmp_Flag :
            string = string + tmp + '=' + "'"
            Jmp_Flag = not Jmp_Flag
        else :
            string = string + tmp + "',"
            Jmp_Flag = not Jmp_Flag

    string = string[0:len(string)-1]
    return string

def makeSelectLine(*args):#别看了就是抄的前边的函数
    string = ''
    for temp in args:
        string = string + str(temp) + ','
    string = string[0:len(string)-1]
    return string##返回类似i,am,a,sb的字符串

def makeSelectIndex(*args):#我再抄一份嘻嘻
    string = ''
    for temp in args :
        string = string + str(temp) + ','
    string = string[0:len(string)-1]
    return string##返回类似i,am,a,sb的字符串

def securitySQL(sql:str):
    sql = sql.upper()

    flag1 = sql.find('--')
    flag2 = sql.find(';')
    flag3 = sql.find('DROP')
    flag4 = sql.find('EXEC')
    flag5 = sql.find('UNION')
    flag6 = sql.find('AND')
    flag7 = sql.find('NULL')
    flag8 = sql.find("VERSION")

    if not (flag1 or flag2 or flag3 or flag4 or flag5 or flag6) :
        if not (flag7 or flag8) :
            return 'Insecure'
        else:
            return 0
    else :
        return 0
