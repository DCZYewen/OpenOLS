from core.db import engine, Base
from core.route import get_handler

if __name__ == '__main__':
    print(len(get_handler()), "app loaded")
    while True:
        value = input("是否重置数据库，所有未备份的数据都会丢失(y/n):")
        if value == "y":
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            print("完成")
            break
        elif value == "n":
            print("取消")
            break
        else:
            print("不支持的值，请重新输入")
