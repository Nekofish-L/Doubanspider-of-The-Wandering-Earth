import requests
from bs4 import BeautifulSoup
import sqlite3

hd = {'User-Aagent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
      'Referer':'https://movie.douban.com/subject/26266893/',
      'Cookie':'bid=w5sdJdebY4o; ll="108299"; _vwo_uuid_v2=DCA7BE5C0E54F4617AF84973DE08FA0AA|e88679c79f33280c537df7f4e0b0cd17; ct=y; push_noty_num=0; push_doumail_num=0; ap_v=0,6.0; ps=y; dbcl2="103511018:3+Lt0+eJqN8"; ck=08Cu; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1550026865%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fsource%3Dsuggest%26q%3D%25E6%25B5%2581%25E6%25B5%25AA%25E5%259C%25B0%25E7%2590%2583%22%5D; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=5a49a9f23c3d7a4c.1549973574.3.1550026873.1549983768.',

url = 'https://movie.douban.com/subject/26266893/comments'

def get_comments(start_id, rank):
    '''
    rank = 'h' 'm' 'l'
    '''
    payload = {'start':start_id,
               'sort':'new_score',
               'status':'P',
               'percent_type':rank,  #h m l
               }

    html = requests.get(url, headers = hd, params=payload)
    soup = BeautifulSoup(html.text, "html.parser")
    comments = soup.find_all(class_='comment-item')
    return comments

def get_addtime(url):
    data = requests.get(url, headers = hd)
    soup = BeautifulSoup(data.text, "html.parser")
    time = soup.find(class_='infobox').find(class_='pl')
    return time.text[-12:-2]

def main(rank):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    for start_id in range(0, 500, 20):
        comments = get_comments(start_id, rank)
        for comment in comments:
            start_id = start_id + 1
            commenter = comment.find(class_='comment-info').a.text
            url = comment.find(class_='comment-info').a['href']
            votes = comment.find(class_='votes').text
            text = comment.find(class_='short').text
            addtime = get_addtime(url)
            cur.execute('INSERT INTO '+ 'douban_' + rank + ' VALUES (?,?,?,?,?,?)',(start_id, commenter, url, votes, text, addtime))
    con.commit()
    con.close()

if __name__ == '__main__':
    for rank in ['h','m','l']:
        main(rank)
