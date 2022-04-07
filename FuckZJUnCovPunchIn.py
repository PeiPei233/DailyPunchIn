from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import sys

username = '321'
password = '123'
url = 'https://oapi.dingtalk.com/robot/send?access_token='
province = '浙江省'
city = '杭州市'
district = '西湖区'
atschool = 'Yes'

for argv in sys.argv:
    if argv[0] == '1' and argv[1:] != '':
        username = argv[1:]
    elif argv[0] == '2' and argv[1:] != '':
        password = argv[1:]
    elif argv[0] == '3' and argv[1:] != '':
        url = argv[1:]
    elif argv[0] == '4' and argv[1:] != '':
        province = argv[1:]
    elif argv[0] == '5' and argv[1:] != '':
        city = argv[1:]
    elif argv[0] == '6' and argv[1:] != '':
        district = argv[1:]
    elif argv[0] == '7' and argv[1:] != '':
        atschool = argv[1:]
        
try:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    brower = webdriver.Chrome(options = chrome_options)
    brower.get('https://healthreport.zju.edu.cn/ncov/wap/default/index')
    #登录
    el = brower.find_element(by=By.ID, value="username")
    el.send_keys(username)

    el = brower.find_element(by=By.ID, value='password')
    el.send_keys(password)

    el.send_keys(Keys.ENTER)
    
    #选择是否在校
    if atschool == 'Yes':
        el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[16]/div/div/div[1]/span[1]')
        el.click()
    else:
        el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[16]/div/div/div[2]/span[1]')
        el.click()

    #显示所在地选择框
    brower.execute_script("document.getElementsByName(\"ip\")[0].style.display = 'block';")

    #选择位置
    el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[21]/div/div/select[1]')
    S = Select(el)
    S.select_by_value(province)

    el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[21]/div/div/select[2]')
    S = Select(el).select_by_value(city)

    el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[21]/div/div/select[3]')
    S = Select(el).select_by_value(district)

    #选择家人是否有恙
    el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[23]/div/div/div[2]/span[1]')
    el.click()

    #选择个人承诺
    el = brower.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[35]/div/div/div/span[1]')
    el.click()

    #提交
    el = brower.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/section/div[5]/div/a')
    el.click()

    #确认提交
    try:
        el = brower.find_element(by=By.XPATH, value='/html/body/div[3]/div/div[2]/div[2]')
        el.click()
    except:
        requests.post(url, json = {
            "text": {
                "content":"今日已打卡"
            },
            "msgtype":"text"
        })
    else:
        requests.post(url, json = {
            "text": {
                "content":"打卡成功"
            },
            "msgtype":"text"
        })

    brower.quit()
except:
    requests.post(url, json = {
        "text": {
            "content":"打卡失败"
        },
        "msgtype":"text"
    })
