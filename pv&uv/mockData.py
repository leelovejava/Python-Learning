# coding:utf-8
# 模拟生成数据 写入 data下的pvuvData
import sys
import time
import random


def mock(path):
    date = time.strftime('%Y-%m-%d')

    #     ip = '192.168.'+str(random.randint(0,255))+'.'+str(random.randint(0,255))
    #     ip = '%s%s%s%s'%('192.168.',str(random.randint(0,255)),'.',str(random.randint(0,255)))

    # random.randint(0,255) 0-255的整数的随机数
    list = ['192.168', str(random.randint(0, 255)), str(random.randint(0, 255))]
    # list中每个元素按.隔开
    ip = '.'.join(list)

    # 5位的userID
    userID = getUserId()

    # 地区
    locations = ['beijing', 'shanghai', 'guangzhou', 'shandong', 'shenzhen', 'chongqing']
    #       random.randint(0,5) 包含0，包含5
    location = locations[random.randint(0, 5)]

    for j in range(0, random.randint(1, 10)):
        # 访问的网站
        websites = ['www.baidu.com', 'www.xiaomi.com', 'www.jd.com', 'www.taobao.com', 'www.qq.com', 'www.360.com',
                    'www.dangdang.com']
        website = websites[random.randint(0, 6)]

        # 操作
        operations = ['register', 'view', 'login', 'logout', 'buy', 'comment', 'jump']
        operation = operations[random.randint(0, 6)]

        oneInfo = date + '\t' + ip + '\t' + "uid" + userID + '\t' + location + '\t' + website + '\t' + operation
        print(oneInfo)
        writeLogToFile(path, oneInfo)


# 获取用户id
def getUserId():
    id = str(random.randint(0, 99999))
    tmpStr = ""
    # id的长度小于5,用0补位
    if len(id) < 5:
        for i in range(0, (5 - len(id))):
            tmpStr += "0"
    return tmpStr + id


# 将日志写到文件
def writeLogToFile(path, log):
    # 'r'：读 'w'：写 'a'：追加
    # 'r+' == r+w（可读可写，文件若不存在就报错(IOError)）
    # 'w+' == w+r（可读可写，文件若不存在就创建）
    # 'a+' ==a+r（可追加可写，文件若不存在就创建）
    # 对应的，如果是二进制文件，就都加一个b： rb'　　'wb'　　'ab'　　'rb+'　　'wb+'　　'ab+'
    with open(path, 'a+') as f:
        f.writelines(log + '\n')


if __name__ == '__main__':
    # 写入当前路径 Params ./pvuvdata
    outputPath = sys.argv[1]
    # sys.argv【1】 取第一号位参数
    # sys.argv[0] 当前文件的路径

    # 从1开始 循环1万次
    for i in range(1, 10000):
        mock(outputPath)
