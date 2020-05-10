import csv, jieba, re
from itertools import islice
import pandas as pd
import imageio
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

# 从导出的csv格式聊天记录中提取中文存入txt文件中
def csv_to_txt():
    chat_csv = open("my_chat.csv","r",encoding="utf-8") #chatlog.csv 改成自己的聊天记录文件名
    my_chat = csv.reader(chat_csv)
    fp = open("chat.txt", "w+", encoding="utf-8")
    for line in islice(my_chat, 1, None):
        if re.search("[\u4e00-\u9fa5]", line[8]) and len(line[8]) < 50:
            fp.write(line[8] + "\n")
    fp.close()


# 对聊天记录文件进行分词
def cut_words():
    # 把聊天内容读取给content
    fp = open("chat.txt", "r", encoding="utf-8")
    content = fp.read()
    fp.close()
    jieba.load_userdict("custom_dict.txt")  # 载入自定义词典（格式：一个词占一行；每行分为：词语、词频（可省略）、词性（可省略），用空格隔开）
    words = jieba.cut(content)  # 进行分词，模式：精确模式
    word_L = []  # 把分词结果存入word_L中
    # 加载停用词
    with open("stopwords.txt", 'r', encoding="utf-8") as ss:
        stopwords = ss.read()
    # 把符合的词语存入word_L中
    for word in words:
        if word not in stopwords and word != '\n' and len(word) > 1:
            word_L.append(word)
    return word_L


# 生成词云
def word_cloud(words):
    # 对分词结果进行频率统计再转换成字典
    count_word_df = pd.DataFrame({"word":words}).groupby(["word"]).size()
    count_word_dt = count_word_df.to_dict()
    mk = imageio.imread('my_pic.jpg')  # 设置词云形状
    mk_color = ImageColorGenerator(mk)  # 设置词云颜色
    # 配置词云参数
    wx_wc = WordCloud(
        background_color="white",  # 如果是透明背景，设置background_color=None
        mode="RGB",  # 如果是透明背景，设置mode="RGBA"
        mask=mk,  # 词云形状
        font_path="青鸟华光简胖头鱼.TTF",  # 字体可以更改为自己喜欢的字体，在C:\Windows\Fonts文件夹
        scale=3,  # 如果输出图片大小不满意，则修改此值
    )
    wx_wc = wx_wc.generate_from_frequencies(count_word_dt)  # 把带频率的分词结果导入词云
    wx_wc.to_file("wordcloud.png")  # 输出词云图片，未设置颜色

    # plt输出图片
    plt.axis("off")  # 关闭坐标轴
    plt.imshow(wx_wc.recolor(color_func=mk_color)) # 设置颜色
    plt.savefig('pltwordcloud.png', dpi=400)  # 输出词云图片，以原图片为背景色


def run():
    csv_to_txt()
    words = cut_words()
    word_cloud(words)

if __name__ == '__main__':
    run()
