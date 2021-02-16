import json
import time
import requests
from selenium import webdriver

#输入自己的账号密码
username=''
password=''

baseapi = "https://api.2dland.cn"


def get_token():
    data = {"ts": "123"}
    r = requests.post(baseapi + "/v3/user/createDestination", data=data)
    str1 = str(r.content, encoding="utf-8")
    token = eval(str1)["destination"]
    return token

//官方取消了账号密码直接登录的api,只能通过浏览器登录
def login(token):
    login_url = "https://account.6pan.cn/login?destination=%s&appid=bc088aa5e2ad&response=query&state=1234&lang=zh-CN"\
                % (token)
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    driver.get(login_url)
    time.sleep(0.5)
    driver.find_element_by_name('username').send_keys(username)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath('//*[@id="root"]/div/div[1]/div/div[2]/div[4]/button').click()
    time.sleep(2)
    # 登录界面是没有cookie的，随便调用一个api就有了
    driver.get("https://api.2dland.cn/v3/newfile/list")
    raw_cookies = driver.get_cookies()
    cookie = "locale=%s;token=%s;token.sig=%s" % (
    raw_cookies[0]["value"], raw_cookies[2]["value"], raw_cookies[1]["value"])
    driver.close()
    return cookie


def parse(headers,link):
    data = {"textLink":link}
    r = requests.post(baseapi + "/v3/offline/parse", headers=headers, data=data)
    str1 = str(r.content, encoding="utf-8")
    hashcode = eval(str1)["hash"]
    return hashcode

def add_offline_task(headers,hashs):
    data = {
        "task": hashs,
        "savePath": "/"
    }
    r = requests.post(baseapi + "/v3/offline/add", headers=headers, data=json.dumps(data))
    str1 = str(r.content, encoding="utf-8")
    num = eval(str1)["successCount"]
    return num

def submit(links):
    token=get_token()
    cookie=login(token)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        "Cookie": cookie
    }
    hashs=[]
    for i in links:
        hashs.append({'hash':parse(headers,i)})
    headers['Content-Type'] = 'application/json'
    successNum=add_offline_task(headers,hashs)
    print("成功添加了%d个任务"%successNum)


if __name__ == '__main__':
	links=["http://feifei.hongjiaozuida.com/20210116/15386_27a530d9/旺达幻视第一季-01.mp4","http://feifei.hongjiaozuida.com/20210116/15387_8b492f74/旺达幻视第一季-02.mp4","http://feifei.hongjiaozuida.com/20210123/15717_30fb9294/旺达幻视第一季-03.mp4"]
    submit(links)