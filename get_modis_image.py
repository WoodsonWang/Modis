import requests
import sys
import time
from io import StringIO
import csv
import os

# python laads-data-download.py -s 订单网址 -d 影像存储目录 -t 用户token

class HtmlRobot():
    def __init__(self,token):
        self.__user_agent = 'tis/download.py_1.0--' + sys.version.replace('\n', '').replace('\r', '')
        self.__headers = {
            'User-Agent':self.__user_agent,
            'Authorization': 'Bearer ' + token
        }

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self,headers):
        self.__headers = headers

    def get_html_head(self,url):
        return requests.head(url,headers=self.__headers).headers

    def get_html(self,url,headers=True,stream=None):
        if headers is True:
            return requests.get(url,headers = self.__headers,stream=stream)
        else:
            return requests.get(url)

    def save(self,url,name):
        ress = self.get_html_head(url)
        total = int(ress['Content-Length'])

        with robot.get_html(url, stream=True) as res:
            # 保存
            sum = 0
            with open('data/'+name,'w+b') as f:
                s = time.time()
                for chunk in res.iter_content(1024*10):

                    if chunk:
                        f.write(chunk)
                        sum += len(chunk)
                        e = time.time()
                        # 剩余时间
                        remaining = int(((total/sum)-1)*(e-s))
                        print('\r'+'{:.2%}已经运行{},剩余时间{}'.format((sum/total),seconds2time(int(e-s)),seconds2time(remaining)),end='')
        print('\n')

    def download(self,order):
        '''解析用户订单，下载影像'''
        # 网址后面有/ 可以直接跟.csv 拼接
        content = self.get_html(order + '.csv')
        reader = csv.DictReader(StringIO(content.content.decode('utf-8')), skipinitialspace=True)
        for f in reader:
            file_url = os.path.join(order, f['name'])
            print(file_url)
            print('正在下载....{}'.format(f['name']))
            self.save(file_url, f['name'])


def seconds2time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '{:0>2d}:{:0>2d}:{:0>2d}'.format(h, m, s)


if __name__ == '__main__':
    # 首先创建data文件夹，影像默认保存到该文件夹下面
    # 改为你自己设置的app-key
    token = ''
    # 改为你自己的订单网址
    order = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/orders/501442420/'

    robot = HtmlRobot(token)
    robot.download(order)




