import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sqlite3
sns.set_style('darkgrid')

def read_from_sql(rank):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute('SELECT addtime FROM douban_' + rank)
    results = cur.fetchall()
    con.close()
    timelist = []
    for result in results:
        time = datetime.strptime(result[0], '%Y-%m-%d')
        timelist.append(time)
    return timelist


if __name__ == '__main__':
    for rank in ['h','m','l']:
        timelist = read_from_sql(rank)

        # sns.distplot(works['高峰小时'], color='#ff8000')
        # plt.show()
        year=[]
        for i in range(0,len(timelist)):
            year.append(timelist[i].year+timelist[i].month/12)

        sns.set(rc={"figure.figsize": (10, 6)})
        ax = sns.distplot(year,
                     color='#ff8000',
                     axlabel='Year',
                     kde_kws={"lw": 3, "label": "distri_" + rank},)

        #ax.set_xticks([2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020])
        ax.set_xticks([2004,2006,2008,2010,2012,2014,2016,2018,2020])
        plt.savefig('流浪地球' + rank + '.png', dpi=300)
        plt.show()
