# Doubanspider-of-The-Wandering-Earth
流浪地球的豆瓣短评爬虫＋简单的数据可视化

## 各部分简介:

```
1. douban.py : 爬虫本体，依赖于requests和bs4实现，并将抓取数据存储于sqlite中。使用时需要填写Cookie。
2. ciyun.py : 对抓取数据中不同评分的评论文本进行分析，并制作词云图。h,m,l分别代表好评、一般和差评。
3. time_distri.py : 对不同评分的评论者注册时间进行分析，得出时间分布柱状图和概率密度图。
```

## 运行环境:
```
python 3.6.4
```
