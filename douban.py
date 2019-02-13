import requests
from bs4 import BeautifulSoup
import sqlite3

hd = {'User-Aagent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
      'Referer':'https://movie.douban.com/subject/26266893/',
      'Cookie':'Your Cookie',}
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
            cur.execute('INSERT INTO '+ 'douban_' + rank + ' VALUES (?,?,?,?,?,?,?)',(start_id, commenter, url, votes, text, addtime, comment_time))
    con.commit()
    con.close()

if __name__ == '__main__':
    for rank in ['h','m','l']:
        main(rank)
