import urllib.request
import re
import random
import time
import os

# 京东商品爬虫
# 爬取京东的商品、价格、出售方、评论数
keyname = "零食"  # 搜索的关键词
key = urllib.request.quote(keyname)  # 关键词转换为URL编码


def getID(url):
    data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
    id_pat = '<strong class="J_(.*?)" '
    return re.compile(id_pat).findall(data)


def getPurllist(id_list, url):
    Purllist = [""] * len(id_list)
    for id in range(0, len(id_list)):
        Purl = "http://item.jd.com/" + id_list[id] + ".html"
        Purllist[id] = Purl
    return Purllist


def getPnamelist(Purllist):
    try:
        Pnamelist = [""] * len(Purllist)
        Pnamelist_tmp = [""] * len(Purllist)
        print("本页一共有" + str(len(Purllist)) + "个商品！！！")
        for i in range(0, len(Purllist)):
            thisPurl = Purllist[i]
            # print("正在爬取："+thisPurl)
            # 正在爬取：http://item.jd.com/6162164.html
            data = urllib.request.urlopen(thisPurl).read().decode("gbk", "ignore")
            # print(data)

            # 标题
            Pname_pat = '<title>.*?】(.*?)【.*?</title>'
            # Pnamelist_tmp=re.compile(Pname_pat).findall(data)
            re_title=re.compile(Pname_pat).findall(data)
            if (re_title):
                Pnamelist[i] = re_title[0]
            else:
                Pnamelist[i] = ""
            # print(Pnamelist[i]+"   第"+str(i+1)+"个商品名")

            # 爬取图片
            # 正则匹配图片
            # https://m.360buyimg.com/babel/s579x579_jfs/t5929/214/7873891577/285498/9679ba96/5982a104N6b827b37.jpg!q100.jpg.webp
            #Pname_pat2 = '<img src="(.*?)" .*?>'
            #if (re.compile(Pname_pat2).findall(data)):
            #    print(re.compile(Pname_pat2).findall(data)[0])

    # print(Pnamelist)
    except Exception as err:
        print(err)
    return Pnamelist

# 获取价格
def getPricelist(url, id_list):
    try:
        labellist = [""] * len(id_list)
        Pricelist = [""] * len(id_list)
        data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        for i in range(0, len(id_list)):
            thisid = id_list[i]
            label_pat = r'<strong class="J_' + thisid + '.*?</strong>'
            Price_pat = '\d+\.\d+'
            labellist[i] = re.search(label_pat, data, re.M).group(0)
            Pricelist[i] = re.search(Price_pat, labellist[i]).group(0)
            # print(Pricelist[i])
    except Exception as err:
        print(err)
    return Pricelist

# 获取商品
def getShoplist(Purllist):
    try:
        Shoplist = [""] * len(Purllist)
        for i in range(0, len(Purllist)):
            thisPurl = Purllist[i]
            # print("正在爬取："+thisPurl)
            data = urllib.request.urlopen(thisPurl).read().decode("gbk", "ignore")
            # print(data)
            # Shop_pat='<h3>.*?title="(.*?)"'
            Shop_pat = '<a href=".*?" target="_blank" title="(.*?)"'
            if (re.compile(Shop_pat).findall(data)):
                Shoplist[i] = re.compile(Shop_pat, re.S).findall(data)[0]
            else:
                Shoplist[i] = "京东自营"
            print("商店名称：" + Shoplist[i])
    # print(Pnamelist)
    except Exception as err:
        print(err)
    return Shoplist

# 获取评论
def getCommentlist(url, id_list):
    try:
        labellist = [""] * len(id_list)
        Commentlist = [""] * len(id_list)
        data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        for i in range(0, len(id_list)):
            thisid = id_list[i]
            # label_pat=r''+thisid+'.*?</strong>'
            label_pat = r'<strong><a id="J_comment_' + thisid + '.*?>(.*?)</a>'
            if (re.compile(label_pat).findall(data)):
                Commentlist[i] = re.compile(label_pat, re.S).findall(data)[0]
            else:
                Commentlist[i] = "无评论"
            # print("评论数量："+Commentlist[i])
    except Exception as err:
        print(err)
    return Commentlist


def mkdir(path):  # 创建文件夹
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


'''主程序'''
mypath = "D:\\spider\\jd\\" + keyname + "\\"
mkdir(mypath)

for pagenum in range(0, 10):
    url = "https://search.jd.com/Search?keyword=" + key + "&enc=utf-8&page=" + str(pagenum + 2)

    print("正在爬取第" + str(pagenum + 1) + "页数据！！！")

    id_list = getID(url)

    Purllist = getPurllist(id_list, url)

    Pnamelist = getPnamelist(Purllist)

    Pricelist = getPricelist(url, id_list)

    Shoplist = getShoplist(Purllist)

    Commentlist = getCommentlist(url, id_list)

    for i in range(0, (len(id_list))):
        print(
            "商品名称：" + Pnamelist[i] + "----商品价格：" + Pricelist[i] + "----出售店铺：" + Shoplist[i] + "----评论数量：" + Commentlist[
                i])
        fh = open("D:\\spider\\jd\\零食\\零食.txt", "a")
        fh.write(
            "商品名称：" + Pnamelist[i] + "----商品价格：" + Pricelist[i] + "----出售店铺：" + Shoplist[i] + "----评论数量：" + Commentlist[
                i] + "\n")

fh.close()
