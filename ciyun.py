import jieba
import jieba.analyse
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import sqlite3

def stop_words(texts):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with open('stopwords.dat','r', encoding='utf-8') as f:
        str_text = f.read() + '地球' + '流浪' + '一部' + '真的'
        unicode_text = bytes(str_text, encoding='utf-8')  # 把str格式转成unicode格式
        f.close()
    for word in word_generator:   # 连续转换word格式
        word = bytes(word, encoding='utf-8')
        if word.strip() not in unicode_text:
            word = str(word, encoding='utf-8')
            words_list.append(word)
    return ' '.join(words_list)

def print_wordcloud(text, photo_name='output.jpg'):
    back_color = imread('earth.jpg')  # 解析该图片
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=600,  # 最大词数
                   mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=110,  # 显示字体的最大值
                   stopwords=STOPWORDS.add('电影'),  # 使用内置的屏蔽词

                   #stopwords=STOPWORDS,
                   font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                   random_state=42,  # 为每个词返回一个PIL颜色
                   # width=1000,
                   # height=860
                   )

    wc.generate(text)
    # 基于彩色图像生成相应彩色
    image_colors = ImageColorGenerator(back_color)
    # 显示图片
    plt.imshow(wc)
    # 关闭坐标轴
    plt.axis('off')
    # 绘制词云
    plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('off')
    # 保存图片
    wc.to_file(photo_name)

# =============================================================================
# try:    # 分析高频词汇出现次数
#     jieba.analyse.set_stop_words('stopwords.dat')
#     tags = jieba.analyse.extract_tags(text, topK = 100, withWeight = True)
#     for item in tags:
#         print(item[0]+'\t'+str(int(item[1]*1000)))
# finally:
#     fp.close()
# =============================================================================
def read_from_sql(rank):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT text FROM douban_' + rank)
    results = cur.fetchall()
    con.close()
    comments = ''
    for result in results:
        comment = ''.join(result)
        comments = comments + comment
    return comments

if __name__ == "__main__":
    for rank in ['h','m','l']:
        text = read_from_sql(rank)
        text = stop_words(text)
        print_wordcloud(text, photo_name='output_' + rank + '.jpg')
