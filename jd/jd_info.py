# 京东手机信息采集：名称、价格、评论数、商家名称等
import requests
from lxml import etree
from pandas import DataFrame
import pandas as pd
import re

# pip install DataFrame

jdInfoAll = DataFrame()
for i in range(1, 4):
    url = "https://list.jd.com/list.html?cat=9987,653,655&page=" + str(i)
    res = requests.get(url)
    res.encoding = 'utf-8'
    root = etree.HTML(res.text)
    name = root.xpath('//li[@class="gl-item"]//div[@class="p-name"]/a/em/text()')
    for i in range(0, len(name)):
        name[i] = re.sub('\s', '', name[i])

    # sku
    sku = root.xpath('//li[@class="gl-item"]/div/@data-sku')

    # 价格
    price = []
    comment = []
    for i in range(0, len(sku)):
        thissku = sku[i]
        priceurl = "https://p.3.cn/prices/mgets?callback=jQuery6775278&skuids=J_" + str(thissku)
        pricedata = requests.get(priceurl)
        pricepat = '"p":"(.*?)"}'
        thisprice = re.compile(pricepat).findall(pricedata.text)
        price = price + thisprice

        commenturl = "https://club.jd.com/comment/productCommentSummaries.action?my=pinglun&referenceIds=" + str(
            thissku)
        commentdata = requests.get(commenturl)
        commentpat = '"CommentCount":(.*?),"'
        thiscomment = re.compile(commentpat).findall(commentdata.text)
        comment = comment + thiscomment

    # 商家名称
    shopname = root.xpath('//li[@class="gl-item"]//div[@class="p-shop"]/@data-shop_name')
    print(shopname)

    jdInfo = DataFrame([name, price, shopname, comment]).T
    jdInfo.columns = ['产品名称', '价格', '商家名称', '评论数']
    jdInfoAll = pd.concat([jdInfoAll, jdInfo])
jdInfoAll.to_excel('jdInfoAll.xls')
