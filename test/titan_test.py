import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool
from values import account_number, card_number, card_password

account_number = account_number() # 账号
card_number = card_number()
card_password = card_password()

# 驱动参数
chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537') #用户中心>>软件ID 生成一个替换 96001
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(ua_pond))
options.add_argument('window-size=1920x1080') #指定浏览器分辨率
# options.add_argument('--headless') # 无界面模式
# options.add_argument('--disable-gpu') # 隐藏gpu界面
# self.options.add_argument('--proxy-server={}'.format(ip_pool))
driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)
# 基本参数
url = 'http://pay.ztgame.com/'

# time.sleep(sleep_time())
driver.get(url)  # 打开网页

# # xss注入参数
driver.find_element_by_xpath('//label[@jslog-trace-id="giantcardgiantpay"]').click() # 点击卡密充值
driver.find_element_by_id('account_ga').send_keys(account_number) # 账号
driver.find_element_by_id('cardno_ga').send_keys(card_number) # 卡号
driver.find_element_by_id('cardpwd_ga').send_keys(card_password)  # 密码

driver.find_element_by_id('btn-trader').click()  # 密码

time.sleep(sleep_time())

print(driver.title)
time.sleep(5)
driver.quit()