import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool, ip_port
from values import account_number, card_number, card_password, choice_sever_SOHU

# from flask import Flask
# from flask import request

# app = Flask(__name__)
# @app.route('/titan/post/api', methods=['POST'])

# account_number = account_number() # 账号
# card_number = card_number()
# card_password = card_password()


class Titan(object):
    '''征途(巨人)充值入口'''
    def __init__(self):
        # 驱动参数
        self.chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537')  # 用户中心>>软件ID 生成一个替换 96001
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--user-agent={}'.format(ua_pond))
        self.options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        self.options.add_argument('--headless') # 无界面模式
        self.options.add_argument('--disable-gpu') # 隐藏gpu界面
        # self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
        # self.driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=self.options)
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=self.options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""})
        # 基本参数
        self.url = 'http://pay.ztgame.com/'

    def parse(self, account_number, card_number, card_password):
        # # xss注入参数
        self.driver.find_element_by_xpath('//label[@jslog-trace-id="giantcardgiantpay"]').click()  # 点击卡密充值
        self.driver.find_element_by_id('account_ga').send_keys(account_number)  # 账号
        self.driver.find_element_by_id('cardno_ga').send_keys(card_number)  # 卡号
        self.driver.find_element_by_id('cardpwd_ga').send_keys(card_password)  # 密码

    def fight(self):
        self.driver.find_element_by_id('btn-trader').click()  # 提交
        statue = {'STATUE': 200, 'MESSAGE': 'SUCCESS'}
        return statue

    def save(self, statue):
        # 获取充值结果
        print(statue)
        print(self.driver.title)
        time.sleep(5)
        self.driver.quit()
        return statue

    def run(self, an, cn, cp):
        time.sleep(sleep_time())
        self.driver.get(self.url)  # 打开网页
        self.parse(an, cn, cp)
        data = self.fight()
        a = self.save(data)
        return a 

# if __name__ == '__main__':
#     pass
    # R = Titan()
    # R.run()
