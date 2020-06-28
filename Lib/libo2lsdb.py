import libconnect

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

conn = libconnect.conn
cur = libconnect.cur

##本库主要为OpenOLS编写，封装了常用的增删改查方法
##只能在单个表内操作

#增
def insertFulline():#提供全行数据的插入
##insertFulline(USERS,makeInsertLine('1','2','3'))
    pass

def insertByRow():#插入在指定的列里（应该没有乱用
##insertByRow(USERS,makeInsertCol(user_id,name,somewhat),makeInsertLine('1','2','3'))
##由于OpenOLS从关系上限制任何键值不能为空，所以这个函数应该是没有卵用，但还是实现了
    pass

#删
def deleteByID():#以ID为索引删除一行
##deleteByID(USERS,114514)
    pass

def deleteByIndex():#删除给定一个删除的索引
##deleteByIndex(USERS,'class',13)把13班的用户都删除
    pass

#改
def updateByID():#以ID为索引修改
##deleteByID(USERS,makeUpdateLine('class',13,'gender','male'),114514)把ID为114514的人的class属性改成13，性别改成male
    pass

def updateByIndex():#索引指定的索引更改
##deleteByIndex(USERS,makeUpdateLine('class',13,'gender','male'),auth,admin)把auth为admin的人的class属性改成13，性别改成male
    pass

#查
## Tips，查找结果一律按ID排序

def selectAll():#只有当生成统计信息时使用，不要调用！
    pass

def selectByID():#根据ID获取一整行数据
##selectByID(USERS,makeSelectLine(user_id,auth),114514)把114514的ID的userid和auth选取出来
##这个函数大概率会用在展示用户列表上
    pass

def selectByIndex():#根据给定的索引选取一整行数据
##selectByIndex(USERS,makeSelectIndex(user_id,114514))这个和上一个函数的实例should do the same 
    pass

def findByValue():#查找一个值
##findByValue():##估计没个鸡儿用，爷懒得写了
##抄一段SQL吧SELECT * FROM Persons WHERE City='Beijing';
    pass

#辅助构造数据结构
def makeInsertLine():
    pass

def makeInsertCol():
    pass

def makeUpdateLine():
    pass

def makeSelectLine():
    pass

def makeSelectIndex():
    pass