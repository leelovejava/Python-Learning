import re
import urllib.request
# 京东商品图片爬虫

def craw(url, page):
    # 读取url地址中的页面
    html1 = urllib.request.urlopen(url).read()
    # 读取url的全部信息并转为字符串
    html1 = str(html1)

    # 匹配元素1---父节点
    pat1 = '<div id="plist".+? <div class="page clearfix">'
    result1 = re.compile(pat1).findall(html1)
    result1 = result1[0]

    # 匹配元素2--子节点
    pat2 = '<img width="220" height="220" data-img="1" data-lazy-img="//(.+?\.jpg)">'

    imagelist = re.compile(pat2).findall(result1)
    x = 1
    for imgurl in imagelist:
        # 设置地址跟爬取图片的地址
        imagename = "D:/spider/jd/img/" + str(page) + str(x) + ".jpg"
        imgurl = "http://" + imgurl
        print(imgurl)
        try:
            # 保存图片并定义图片名字
            urllib.request.urlretrieve(imgurl, filename=imagename)
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                x += 1
            if hasattr(e, "reason"):
                x += 1
        x += 1


for i in range(1, 79):
    url = 'http://list.jd.com/list.html?cat=9987,653,655&page=' + str(i)
    craw(url, i)
