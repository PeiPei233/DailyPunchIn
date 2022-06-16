from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import sys
from time import sleep
from random import random

username = '321'
password = '123'
url = 'https://oapi.dingtalk.com/robot/send?access_token='
latitude = 30.307482568059065 + random() * 1e-4
longtitude = 120.08188799406054 + random() * 1e-4
atschool = 'Yes'

for argv in sys.argv:
    if argv[0] == '1' and argv[1:] != '':
        username = argv[1:]
    elif argv[0] == '2' and argv[1:] != '':
        password = argv[1:]
    elif argv[0] == '3' and argv[1:] != '':
        url = argv[1:]
    elif argv[0] == '4' and argv[1:] != '':
        latitude = float(argv[1:]) + random() * 1e-4
    elif argv[0] == '5' and argv[1:] != '':
        longtitude = float(argv[1:]) + random() * 1e-4
    elif argv[0] == '6' and argv[1:] != '':
        atschool = argv[1:]
        
try:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options = chrome_options)

    #给予网页获取地理位置信息的权限
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": "https://healthreport.zju.edu.cn/ncov/wap/default/index",
            "permissions": ["geolocation"]
        },
    )

    #模拟地理位置信息
    Map_coordinates = dict({
        "latitude": latitude,
        "longitude": longtitude,
        "accuracy": 100
    })
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)

    driver.get('https://healthreport.zju.edu.cn/ncov/wap/default/index')
    
    #登录
    el = driver.find_element_by_id("username")
    el.send_keys(username)

    el = driver.find_element_by_id('password')
    el.send_keys(password)

    el.send_keys(Keys.ENTER)

    #选择是否在校
    # if atschool == 'Yes':
    #     el = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[16]/div/div/div[1]/span[1]')
    #     el.click()
    # else:
    #     el = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/section/div[4]/ul/li[16]/div/div/div[2]/span[1]')
    #     el.click()
    el = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/section/div[4]/ul/li[4]/div/div/div[1]/span[1]')
    el.click()

    #获取位置
    el = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/section/div[4]/ul/li[9]/div/input')
    el.click()

    sleep(5)
    
    #选择个人承诺
    el = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/section/div[4]/ul/li[26]/div/div/div/span[1]')
    el.click()

    #提交
    el = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/div/section/div[5]/div/a')
    el.click()
    
    #确认提交
    try:
        el = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div[2]/div[2]')
        el.click()
    except:
        requests.post(url, json = {
            "text": {
                "content":"今日已打卡"
            },
            "msgtype":"text"
        })
        print("Fail")
    else:
        requests.post(url, json = {
            "text": {
                "content":"打卡成功"
            },
            "msgtype":"text"
        })

    driver.quit()
except:
    requests.post(url, json = {
        "text": {
            "content":"打卡失败"
        },
        "msgtype":"text"
    })
