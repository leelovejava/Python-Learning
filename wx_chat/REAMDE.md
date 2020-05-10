python词云-和女朋友的微信聊天记录

效果图

![效果图](https://attach.52pojie.cn/forum/202004/12/170104f99494db499dcb92.png)

## 一、如何获取聊天记录
1.你需要和谁的聊天记录生成词云，就把和她的聊天记录通过电脑版微信备份一下，然后通过安卓模拟器再把她的聊天记录从 电脑版微信 恢复到 模拟器的微信 里面。

2.通过re或者类似文件管理器找到这个/data/data/com.tencent.mm/MicroMsg路径，下面有一个数字和字母组成名称很长的文件夹，把里面EnMicroMsg.db文件取出到电脑里备用
       
3./data/data/com.tencent.mm/shared_prefs路径下有一个auth_info_key_prefs.xml文件，记住里面的_auth_uin值(这个值可能是9位,10位或者负数)备用
       
4.打开模拟器的设置界面，记住IMEI值
       
5.用你得到的IMEI值 拼接 UIN值（例如IMEI:865166023282877 UIN:1002623291 拼接结果:8651660232828771002623291）放在MD5计算网站加密，得到一个32位小写的值，取前七位
       
6.用 sqlcipher 软件打开之前的第2步得到的EnMicroMsg.db文件(File - Open Database 或者文件直接拖拽进去)，把第5步得到的七位值输进去

7.把聊天记录文件导出为csv格式(File - Export - Table as CSV file),选择message然后点击Export，命名为my_chat.csv，用记事本打开次文件，以utf-8格式保存。
  
![记事本格式](https://attach.52pojie.cn/forum/202004/12/153416hdzikz8hj6yylkhi.png)
    
## 二、需要用到的文件及python库

1. sqlcipher 软件 、电脑版微信 、夜神(雷电等)模拟器

2. stopwords.txt、 custom_dict.txt、 my_chat.csv(第一步获取到的)、my_pic.jpg(网上自行下载喜欢的图片后改名)、青鸟华光简胖头鱼.TTF(本帖效果图字体文件，可以自行选择)

3. python库：jieba pandas matplotlib wordcloud
