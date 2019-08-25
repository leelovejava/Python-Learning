from pyspark import SparkConf, SparkContext

"""
    PySpark统计PV，UV
    1). 统计PV,UV
    2). 统计除了某个地区外的UV
    3). 统计每个网站最活跃的top2地区
    4). 统计每个网站最热门的操作
    5). 统计每个网站下最活跃的top3用户
"""


# python 编译性语言,方法写在main方法前面

def getTop3User(one):
    site = one[0]
    localIterable = one[1]

    # dic字典：计数,类似于scala中的map(k,v)
    localDic = {}

    # 遍历地区
    for local in localIterable:
        # 判断是否在dic中
        if local in localDic:
            localDic[local] += 1
        else:
            localDic[local] = 1

    # 排序 按照Key倒序排序
    # localDic.items() 变成可遍历
    # reverse=True 反转 降序
    sort_list = sorted(localDic.items(), key=lambda tp: tp[1], reverse=True)
    returnResult = []

    # 取top2的地区
    if len(sort_list) > 2:
        for i in range(2):
            returnResult.append(sort_list[i])
    else:
        returnResult = sort_list

    # 返回2元组,相当于tuple
    return site, returnResult

# 统计每个网站下最活跃的top3用户
def getUserCount(one):
    uid = one[0]
    siteIterable = one[1]
    siteDic = {}
    for site in siteIterable:
        if site in siteDic:
            siteDic[site] += 1
        else:
            siteDic[site] = 1
    returnList = []
    for site, count in siteDic.items():
        returnList.append((site, (uid, count)))

    return returnList


def getTop3(one):
    site = one[0]
    uid_count_iterables = one[1]

    top3_uid_count = ["", "", ""]
    for uid_count in uid_count_iterables:
        uid = uid_count[0]
        count = uid_count[1]
        for i in range(3):
            if top3_uid_count[i] == "":
                top3_uid_count[i] = uid_count
                break
            elif top3_uid_count[i][1] < count:
                for j in range(2, i, -1):
                    top3_uid_count[j] = top3_uid_count[j - 1]
                top3_uid_count[i] = uid_count
                break
    return site, top3_uid_count


if __name__ == '__main__':
    conf = SparkConf()
    conf.setMaster("local")
    conf.setAppName("pvuv")

    sc = SparkContext(conf=conf)
    lines = sc.textFile("./pvuvdata")

    # 统计每个网站下最活跃的top3用户
    uid_site = lines.map(lambda one: (one.split("\t")[2], one.split("\t")[4]))
    site_uid_count = uid_site.groupByKey().flatMap(lambda one: getUserCount(one))
    # lambda表达式只能写一行,多行只能写成方法
    site_uid_count.groupByKey().map(lambda one: getTop3(one)).foreach(print)

    # 3). 统计每个网站最活跃的top2地区
    # site_local = lines.map(lambda line:(line.split("\t")[4],line.split("\t")[3]))
    # site_local.groupByKey().map(lambda one:getTop3User(one)).foreach(print)

    # 求uv 独立访客数(unique visitor 按用户id或者ip区分是不是同一个用户)
    # 思路: ip和网址在这一天内,看成是一个 去重之后,对网址计数累加
    # ip_site = lines.map(lambda line:line.split("\t")[1]+"_"+line.split("\t")[4])

    # 2). 统计除了某个地区外的UV
    # ip_site = lines.filter(lambda one:one.split("\t")[3]=='beijing').map(lambda line:line.split("\t")[1]+"_"+line.split("\t")[4])
    # ip_site.distinct().map(lambda one:(one.split("_")[1],1)).reduceByKey(lambda v1,v2:v1+v2).foreach(print)

    # 求pv(page view:页面浏览量)
    # site_count = lines.map(lambda line:(line.split("\t")[4],1))
    # total_site_count = site_count.reduceByKey(lambda v1,v2:v1+v2)
    # 降序 ascending=False
    # total_site_count.sortBy(lambda tp:tp[1],ascending=False).foreach(print)
