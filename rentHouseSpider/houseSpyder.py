import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


class HouseSpider:
    def __init__(self):
        # 1.连接数据库服务器,获取客户端对象
        self.client = MongoClient('mongodb://hadoop000:27017/')
        # self.client = MongoClient('192.168.9.17',27017)
        # zfdb:数据库名
        self.zfdb = self.client.zfdb
        # self.zfdb.authenticate("admin", "admin")

    session = requests.Session()
    baseUrl = "http://sz.zu.fang.com"

    urlDir = {
        "不限": "/house/",
        "宝安": "/house-a089/",
        "龙岗": "/house-a090/",
        "南山": "/house-a087/",
        "福田": "/house-a085/",
        "罗湖": "/house-a086/",
        "盐田": "/house-a088/",
        "龙华区": "/house-a013080/",
        "坪山区": "/house-a013081/",
        "光明新区": "/house-a013079/",
        "大鹏新区": "/house-a013082/",
        "惠州": "/house-a013058/",
        "东莞": "/house-a013057/",
        "深圳周边": "/house-a016375/",
    }
    region = "不限"
    page = 100

    # 通过名字获取 url 地址
    def getRegionUrl(self, name="宝安", page=10):
        urlList = []
        for index in range(page):
            if index == 0:
                urlList.append(self.baseUrl + self.urlDir[name])
            else:
                urlList.append(self.baseUrl + self.urlDir[name] + "i3" + str(index + 1) + "/")

        return urlList

    # MongoDB 存储数据结构
    def getRentMsg(self, title, rooms, area, price, address, traffic, region, direction):
        return {
            # 标题
            "title": title,
            # 房间数
            "rooms": rooms,
            # 平方数
            "area": area,
            # 价格
            "price": price,
            # 地址
            "address": address,
            # 交通描述
            "traffic": traffic,
            # 区、（福田区、南山区）
            "region": region,
            # 房子朝向（朝南、朝南北）
            "direction": direction,
        }

    # 获取数据库 collection
    def getCollection(self, name):
        zfdb = self.zfdb
        if name == "不限":
            return zfdb.rent
        if name == "宝安":
            return zfdb.baoan
        if name == "龙岗":
            return zfdb.longgang
        if name == "南山":
            return zfdb.nanshan
        if name == "福田":
            return zfdb.futian
        if name == "罗湖":
            return zfdb.luohu
        if name == "盐田":
            return zfdb.yantian
        if name == "龙华区":
            return zfdb.longhuaqu
        if name == "坪山区":
            return zfdb.pingshanqu
        if name == "光明新区":
            return zfdb.guangmingxinqu
        if name == "大鹏新区":
            return zfdb.dapengxinqu

    # 区域集合
    def getAreaList(self):
        return [
            "宝安",
            "龙岗",
            "南山",
            "福田",
            "罗湖",
            "盐田",
            "龙华",
            "坪山",
            "光明",
            "大鹏",
        ]

    def getOnePageData(self, pageUrl, reginon="不限"):
        rent = self.getCollection(self.region)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'})
        res = self.session.get(
            pageUrl
        )
        soup = BeautifulSoup(res.text, "html.parser")
        # 获取需要爬取得 div
        divs = soup.find_all("dd", attrs={"class": "info rel"})

        for div in divs:
            ps = div.find_all("p")
            try:  # 捕获异常，因为页面中有些数据没有被填写完整，或者被插入了一条广告，则会没有相应的标签，所以会报错
                for index, p in enumerate(ps):  # 从源码中可以看出，每一条 p 标签都有我们想要的信息，故在此遍历 p 标签，
                    text = p.text.strip()
                    print(text)  # 输出看看是否为我们想要的信息
                print("===================================")
                # 爬取并存进 MongoDB 数据库
                roomMsg = ps[1].text.split("|")
                # rentMsg 这样处理是因为有些信息未填写完整，导致对象报空
                area = roomMsg[2].strip()[:len(roomMsg[2]) - 2]
                rentMsg = self.getRentMsg(
                    ps[0].text.strip(),
                    roomMsg[1].strip(),
                    int(float(area)),
                    int(ps[len(ps) - 1].text.strip()[:len(ps[len(ps) - 1].text.strip()) - 3]),
                    ps[2].text.strip(),
                    ps[3].text.strip(),
                    ps[2].text.strip()[:2],
                    roomMsg[3],
                )
                rent.insert_one(rentMsg)
            except:
                continue

    def setRegion(self, region):
        self.region = region

    def setPage(self, page):
        self.page = page

    def startSpicder(self):
        for url in self.getRegionUrl(self.region, self.page):
            self.getOnePageData(url, self.region)
            print("=================== one page 分割线 ===========================")
            print("=================== one page 分割线 ===========================")
            print("=================== one page 分割线 ===========================")
            time.sleep(5)


spider = HouseSpider()
# 设置爬取页数
spider.setPage(10)
# 设置爬取区域
spider.setRegion("不限")
# 开启爬虫
spider.startSpicder()
