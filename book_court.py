import datetime
import time
from urllib import parse,request
import requests
import json


# 羽毛球一号场
# 发送date
data_info_org = {
    "fdId": 28, #场地分块ID             29:羽毛球三号场
    "beginTime": "2019-03-22 18:00:00", #开始时间
    "endTime": "2019-03-22 20:00:00",   #结束时间
    "ffId": 4,  #场地ID       4:羽毛球   5:乒乓球   6:形体
    "ggId": 2,  #场馆ID       2:风雨
    "usrId": 2384,  #用户ID
    "money": 20.00,  #一小时十块
    "ifPaid": 0,
    "status": 0,
    "ordTime": "2019-03-21 00:00:00",
    "payType": 2
}


#header信息
headers_org = {"Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Length": "169",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "JSESSIONID=39F5477C6E529D4297C46929E7B596AB",            #Cookie 每次登录需要更新
            "Host": "gym.whu.edu.cn",
            "Origin": "http://gym.whu.edu.cn",
            "Pragma": "no-cache",
            "Referer": "http://gym.whu.edu.cn/wechat/booking/gymHome.jsp",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"}


'''
info_data:
headers:
Cookie:
'''
def book_court(info_data, headers, Cookie):
    url = 'http://gym.whu.edu.cn/OrderAction!bookOrder?deposit=0.00'
    headers['Cookie'] = Cookie
    fd_ids = [27, 28, 29, 30, 31, 32]   #遍历所有场地，抢到break
    for fd_id_tmp in fd_ids:
        info_data['fdId'] = (int)(fd_id_tmp)
        try:
            response = requests.post(url, data=info_data, headers=headers)
            print(response.text)
            if response.status_code == 200 and response.text != -1 and response.text != '-1':
                print("book succ! fd_id is %d" %fd_id_tmp)
                break
        except Exception as e:
            print(e)


if __name__ == '__main__':

    #计时器
    time_new = datetime.datetime.strptime("2018-12-29-00-00-00", '%Y-%m-%d-%H-%M-%S')
    time_old = datetime.datetime.now()

    while (time_old < time_new):
        print(time_old.strftime('%Y-%m-%d-%H-%M-%S') + "    wait for timing")
        time.sleep(1)
        time_old = datetime.datetime.now()

    print("start trying to book court")
    #手动获取cookie
    Cookie = "JSESSIONID=C2A0569C896461360421A564CC177C85"
    book_court(info_data=data_info_org, headers=headers_org, Cookie=Cookie)