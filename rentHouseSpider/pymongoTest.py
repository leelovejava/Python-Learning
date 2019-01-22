# !/usr/bin/env python
# -*- coding:utf-8 -*-


"""
使用pymongo库操作MongoDB数据库
"""

import pymongo

# 1.连接数据库服务器,获取客户端对象
mongo_client = pymongo.MongoClient('hadoop000', 27017)

# 2.获取数据库对象
db = mongo_client.myDB
# db=mongo_client['myDB']

# 3.获取集合对象
my_collection = db.zfdb

print("——" * 50)
# 插入文档
tom = {'name': 'Tom', 'age': 18, 'sex': '男', 'hobbies': ['吃饭', '睡觉', '打豆豆']}
alice = {'name': 'Alice', 'age': 19, 'sex': '女', 'hobbies': ['读书', '跑步', '弹吉他']}
tom_id = my_collection.insert_one(tom)
alice_id = my_collection.insert_one(alice)
print(tom_id)
print(alice_id)

print("——" * 50)
# 查询文档
cursor = my_collection.find()
print(cursor.count_documents())  # 获取文档个数
for item in cursor:
    print(item)

print("——" * 50)
# 修改文档
my_collection.update_one({'name': 'Tom'}, {'$set': {'hobbies': ['向Alice学习读书', '跟Alice一起跑步', '向Alice学习弹吉他']}})
for item in my_collection.find():
    print(item)

print("——" * 50)
# 删除文档
# my_collection.remove({'name':'Tom'},{'justOne':0})
my_collection.delete_one()
for item in my_collection.find():
    print(item)
