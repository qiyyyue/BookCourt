import datetime
import time
import requests
import json
import urllib.request
import urllib.parse
import http.cookiejar
import re



class Book_Court():


    def __init__(self, _name, _password, _date, _ggId = 2, _ffId = 4):
        '''
        初始化
        :param _name: 用户名
        :param _password: 密码
        :param _date: 日期    年-月-日
        :param _ggId: 场馆id  2: 风雨
        :param _ffId: 场地id  4: 羽毛球
        '''
        self.name = _name
        self.password = _password

        self.ggId = _ggId
        self.ffId = _ffId

        self.date = _date.strftime('%Y-%m-%d')

    def get_cookie(self):
        '''
        获取cookie
        :return: None
        '''
        # 登录的主页面
        hosturl = 'http://gym.whu.edu.cn'

        # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
        cj = http.cookiejar.LWPCookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

        # 打开登录主页面（目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
        hostOpen = urllib.request.urlopen(hosturl)

        # 解析cookie
        cookieText = ''
        for item in cj:
            cookieText = cookieText + item.name + '=' + item.value + '&'
        cookieText = cookieText[0:-1]

        self.cookie = cookieText

    def log_in(self):
        '''
        模拟登陆, cookie生效
        :return: None
        '''
        url = 'http://gym.whu.edu.cn/loginAction!UserLogin'
        req_data = {'name': self.name, 'password': self.password}
        req_headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Content-Length": str(len(urllib.parse.urlencode(req_data))),
                   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                   "Cookie": self.cookie,  # Cookie
                   "Host": "gym.whu.edu.cn",
                   "Origin": "http://gym.whu.edu.cn",
                   "Referer": "http://gym.whu.edu.cn/wechat/booking/gymHome.jsp",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                   "X-Requested-With": "XMLHttpRequest"}

        res = requests.post(url, data = req_data, headers = req_headers)

    def get_userId(self):
        '''
        获取usrId
        :return: None
        '''
        url = "http://gym.whu.edu.cn:80/wechat/booking/gymHome.jsp?ggId=" + str(self.ggId)
        req_headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Connection": "keep-alive",
                   "Cookie": self.cookie,  # Cookie
                   "Host": "gym.whu.edu.cn",
                   "Referer": "http://gym.whu.edu.cn/wechat/map/mapHome.jsp",
                   "Upgrade - Insecure - Requests": '1',
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                   "X-Requested-With": "XMLHttpRequest"}

        res = requests.get(url, headers = req_headers)
        match_res = re.search(r'\"usrId\"\:(\d+),', str(res.text))

        self.userId = int(match_res.group(1))


    def get_gym_name(self):
        '''
        获取场馆名字
        :return:
        '''
        url = 'http://gym.whu.edu.cn/OrderQueryAction!getGymNameByGgId'
        req_data = {'ggId': self.ggId}
        req_headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                       "Accept-Encoding": "gzip, deflate",
                       "Accept-Language": "zh-CN,zh;q=0.9",
                       "Connection": "keep-alive",
                       "Content-Length": str(len(urllib.parse.urlencode(req_data))),
                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "Cookie": self.cookie,  # Cookie
                       "Host": "gym.whu.edu.cn",
                       "Origin": "http://gym.whu.edu.cn",
                       "Referer": "http://gym.whu.edu.cn/wechat/booking/gymHome.jsp?ggId={}".format(self.ggId),
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                       "X-Requested-With": "XMLHttpRequest"}

        res = requests.post(url, data=req_data, headers=req_headers)

        print(res.text)

    def get_gym_items(self):
        '''

        :return:
        '''
        url = 'http://gym.whu.edu.cn/OrderQueryAction!getGymItems'
        req_data = {'ggId': self.ggId,
                    'date': self.date}
        req_headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                       "Accept-Encoding": "gzip, deflate",
                       "Accept-Language": "zh-CN,zh;q=0.9",
                       "Connection": "keep-alive",
                       "Content-Length": str(len(urllib.parse.urlencode(req_data))),
                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "Cookie": self.cookie,  # Cookie
                       "Host": "gym.whu.edu.cn",
                       "Origin": "http://gym.whu.edu.cn",
                       "Referer": "http://gym.whu.edu.cn/wechat/booking/gymHome.jsp?ggId={}".format(self.ggId),
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                       "X-Requested-With": "XMLHttpRequest"}

        res = requests.post(url, data=req_data, headers=req_headers)

        print(res.text)

    def get_court_info(self):
        '''
        获取场馆场地信息
        json  [i,j] i行j列
        status: 0未定  1已定
        :return:
        '''
        url = 'http://gym.whu.edu.cn/OrderQueryAction!getMPointPeriod'
        req_data = {'ggId': self.ggId,
                    'ffId': self.ffId,
                    'usrId': self.userId,
                    'date': self.date,
                    'startTime': '00:00:00',
                    'endTime': '23:59:00'}
        req_headers = {"Accept": "*/*",
                       "Accept-Encoding": "gzip, deflate",
                       "Accept-Language": "zh-CN,zh;q=0.9",
                       "Connection": "keep-alive",
                       "Content-Length": bytes(len(urllib.parse.urlencode(req_data))),
                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "Cookie": self.cookie,  # Cookie
                       "Host": "gym.whu.edu.cn",
                       "Origin": "http://gym.whu.edu.cn",
                       "Referer": "http://gym.whu.edu.cn/wechat/booking/gymHome.jsp?ggId={}".format(self.ggId),
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                       "X-Requested-With": "XMLHttpRequest"}

        res = requests.post(url, data=req_data, headers=req_headers)

        _book_status = res.json()

        # status = [[1 for _ in range(len(_book_status[0]))] for _ in range(len(_book_status))]
        #
        # for i in range(len(_book_status)):
        #     for j in range(len(_book_status[0])):
        #         item = _book_status[i][j]
        #         status[i][j] = item['status']

        #打印订阅信息
        # for i in range(len(status)):
        #     for j in range(len(status[0])):
        #         print("{}\t".format(status[i][j]), end='')
        #     print()

        self.book_status = _book_status

    def book_court(self, start_time = '00:00', max_time = 24.0, end_time = '21:00'):
        '''
        订场地
        :param start_time: 最早开始时间   时-分
        :param max_time: 最晚开始时间     时-分
        :param end_time: 最长持续时间     小时数, 小树
        :return:
        '''

        date_formate = '%H:%M'

        #最早可接受的空场时间, i表示行数
        start_i = 0
        for i in range(len(self.book_status)):
            if time.strptime(self.book_status[i][0]['startTime'], date_formate) >= time.strptime(start_time, date_formate):
                start_i = i
                break

        max_s_i = start_i   #开始时间
        max_e_i = start_i   #结束时间
        max_len_i = 0       #持续时间
        max_j = 0           #列数

        #查询场地状态,获取满足要求,时常最长的场地信息
        #j表示列数,i表示行数
        for j in range(len(self.book_status[0])):
            for i in range(start_i, len(self.book_status)):
                if self.book_status[i][j]['status'] == 1:
                    continue
                end_i = i
                while end_i + 1 < len(self.book_status) and self.book_status[end_i + 1][j]['status'] == 0:
                    end_i += 1
                    if time.strptime(self.book_status[end_i][j]['endTime'], date_formate) >= time.strptime(end_time, date_formate):
                        break
                    if datetime.datetime.strptime(self.book_status[i][j]['startTime'], date_formate) + datetime.timedelta(hours = max_time) >= datetime.datetime.strptime(self.book_status[end_i][j]['endTime'], date_formate):
                        break
                if end_i - i > max_len_i:
                    max_s_i = i
                    max_e_i = end_i
                    max_len_i = end_i - i
                    max_j = j

        if max_len_i == 0:
            print('没有符合要求的场地')
            return -1


        # construct headers and data
        fdId = self.book_status[max_s_i][max_j]['fdId']
        beginTime = self.date + " " + self.book_status[max_s_i][max_j]['startTime'] + ":00"
        endTime = self.date + " " + self.book_status[max_e_i][max_j]['endTime'] + ":00"
        money = 0.0
        for i in range(max_s_i, max_e_i + 1):
            money += self.book_status[i][max_j]['money']
        ordTime =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        url = 'http://gym.whu.edu.cn/OrderAction!bookOrder?deposit=0.00'

        req_data = {
            "fdId": fdId,  # 场地分块ID
            "beginTime": beginTime,  # 开始时间
            "endTime": endTime,  # 结束时间
            "ffId": self.ffId,  # 场地ID       4:羽毛球   5:乒乓球   6:形体
            "ggId": self.ggId,  # 场馆ID       2:风雨
            "usrId": self.userId,  # 用户ID
            "money": money,  #
            "ordTime": ordTime,
            "payType": 2
        }

        headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                       "Accept-Encoding": "gzip, deflate",
                       "Accept-Language": "zh-CN,zh;q=0.9",
                       "Cache-Control": "no-cache",
                       "Connection": "keep-alive",
                       "Content-Length": bytes(len(urllib.parse.urlencode(req_data))),
                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                       "Cookie": self.cookie,  # Cookie 每次登录需要更新
                       "Host": "gym.whu.edu.cn",
                       "Origin": "http://gym.whu.edu.cn",
                       "Pragma": "no-cache",
                       "Referer": "http://gym.whu.edu.cn/wechat/booking/gymHome.jsp",
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                       "X-Requested-With": "XMLHttpRequest"}

        # print('---------------')
        # print(req_data)

        # try requests
        try_count = 0
        try:
            response = requests.post(url, data=req_data, headers=headers)
            print(response.text)
            if response.status_code == 200 and response.text != -1 and response.text != '-1' and response.json()['status'] == 0:
                print("book succ!")
                print("startTime:{}\tendTime{}\t{}号场".format(beginTime, endTime, max_j+1))
            else:
                try_count += 1
                if try_count == 10:
                    print('没有符合要求的场地')
                    return -1
                self.book_court(start_time, max_time, end_time)
        except Exception as e:
            print(e)
            try_count += 1
            if try_count == 10:
                print('没有符合要求的场地')
                return -1
            self.book_court(start_time, max_time, end_time)


if __name__ == '__main__':

    name = 'qiyyyue'
    password = 'Lee951012'

    date = datetime.datetime(2019, 5, 24)   #目标日期
    ddl = date + datetime.timedelta(days=-2, hours=18)    #开放时间

    #计时器
    time_now = datetime.datetime.now()
    while (time_now < ddl):
        print(time_now.strftime('%Y-%m-%d %H:%M:%S') + ",\twait for timing,\t" + ddl.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(1)
        time_now = datetime.datetime.now()

    print("start trying to book court")

    #
    bc = Book_Court(name, password, date)
    bc.get_cookie()
    bc.log_in()
    bc.get_userId()
    bc.get_court_info()
    bc.book_court(start_time='10:00')
