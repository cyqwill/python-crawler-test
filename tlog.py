import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import datetime

import proxy


class Tlog(object):
    """
    自定义游记类，暂时就是参数信息
    """
    def __init__(self, url):
        self.url = url
        self.error = None
        # 由url解析id
        try:
            log_id = url.split('/i/')[1]
            # 去掉.html
            log_id = log_id.split('.')[0]
            self.log_id = int(log_id)
        except IndexError:
            self.error = 'Url format is wrong.'
        except ValueError:
            self.error = 'Log id format is wrong.'

    def download_content(self):
        """
        下载对应页面的内容
        """
        ua = UserAgent()
        # 检查url是否为标准的地址格式, 换正则mafengwo.cn/i/\d+$
        if r'mafengwo.cn/i/' not in self.url:
            return
        r = requests.get(self.url, ua.chrome, proxies=proxy.proxies)
        if r.status_code == 200:
            self.html = r.content.decode('utf-8')
            self.parse_content()


    def parse_content(self):
        """
        解析html页面内容
        """
        if self.html is None:
            return
        # 使用bs解析
        html_bs_obj = BeautifulSoup(self.html, 'lxml')
        try:
            # 大标题
            self.title = html_bs_obj.select('h1')[0].text.strip()
            # 文字内容
            self.text_content = html_bs_obj.find(class_='va_con').text
            self.text_content = ''.join(self.text_content.split())
        except IndexError:
            self.error = 'Parse content error. Index out of range.'
        except AttributeError:
            self.error = 'Parse content error. No attribute.'
        print('已抓取:', self.title)
        # 如果时间，天数等非必要参数问题，可以忽略,使用标记值
        try:
            # 出发时间
            start_time = html_bs_obj.select('.time')[0].text.split(r'/')[1]
            # 转datetime
            self.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        except:
            self.start_time = datetime.datetime(1900, 1, 1, 0, 0)
        try:
            # 出行天数
            days = html_bs_obj.select('.day')[0].text.split(r'/')[1]
            # 转int
            self.days = int(days.split('天')[0])
        except:
            self.days = -1


    def to_string_for_save(self):
        """
        为了存储为文件，将所有属性转换为字符串
        """
        if not self.error:
            return '{}^{}^{}^{}^{}^{}'.format(self.title,
                                              self.start_time,
                                              self.days,
                                              self.text_content,
                                              self.url,
                                              self.html)
        else:
            return ''


    def to_dict(self):
        """
        :return: 返回字典类型的对象
        """
        if not self.error:
            dict_obj = {'log_id': self.log_id,
                        'title': self.title,
                        'start_time': self.start_time,
                        'days': self.days,
                        'text_content': self.text_content,
                        'url': self.url,
                        'html': self.html}
            return dict_obj
        else:
            print(self.error)
            return None
