import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool
from values import account_number, card_number, card_password, choice_sever_SOHU, neteasy_email_password, \
    will_topup_number

account_number = account_number() # 账号
card_number = card_number()
card_password = card_password()

# 驱动参数
chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537') #用户中心>>软件ID 生成一个替换 96001
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(ua_pond))
options.add_argument('window-size=1920x1080') #指定浏览器分辨率
options.add_argument('--headless') # 无界面模式
options.add_argument('--disable-gpu') # 隐藏gpu界面
# self.options.add_argument('--proxy-server={}'.format(ip_pool))
driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)
# 基本参数
url = 'https://star.game.163.com/xyq/'
# url = 'http://ecard.163.com/card_login?refer_uri=%2Fecard'

# time.sleep(sleep_time())
driver.get(url)  # 打开网页

# 登陆
time.sleep(3)
try:
    # driver.find_element_by_xpath('//a[@class="login_btn"]').click()
    element = driver.find_element_by_xpath('//a[@class="login_btn"]')
    driver.execute_script("arguments[0].click();", element)
    print('-----登陆已经点击-----')
except Exception as e:
    print(e)

# iframe = driver.find_element_by_xpath('//div[@id="urs-login-block"]/iframe') # 正门
try:
    iframe = driver.find_element_by_xpath('//div[@id="email_login"]/iframe') # 侧门1
    driver.switch_to.frame(iframe)
    t_iframe = driver.find_element_by_xpath('//div[@id="login-base"]/iframe') # 侧门2
    driver.switch_to.frame(t_iframe)
    print('-----进门成功!-----')
except:
    print('没进去门 -.= ')
try:
    driver.find_element_by_xpath('//div[@data-action="goEmailLogin"]').click() # 切换句柄
    print('-----切换成功!-----')
except Exception as e:
    print(e)
    print('没订上')
try:
    driver.find_element_by_xpath('//input[@data-placeholder="请输入帐号"]').clear()
    driver.find_element_by_xpath('//input[@data-placeholder="请输入帐号"]').send_keys(neteasy_email_password('账号'))
    driver.find_element_by_xpath('//input[@data-placeholder="请输入密码"]').clear()
    driver.find_element_by_xpath('//input[@data-placeholder="请输入密码"]').send_keys(neteasy_email_password('密码'))
    print('-----添加账号密码成功!-----')
except Exception as e:
    print(e)
    print('选不上东西')
try:
    driver.find_element_by_id('dologin').click()
    print('-----登陆成功!-----')
except Exception as e:
    print(e)
    print('登陆失败')
try:
    driver.switch_to.default_content() # 退出iframe
    print('-----默认退出成功!-----')
except:
    print('退出失败')

# 切换至充值页面
driver.find_element_by_xpath('//a[@title="官网"]').click() # 跳转至官网

# 1. 获取当前所有的窗口
windows = driver.window_handles
time.sleep(2)
driver.switch_to.window(windows[1])
print('-----窗口2!-----')

driver.find_element_by_xpath('//a[text()="快速充值"]').click()
time.sleep(1)
windows = driver.window_handles
driver.switch_to.window(windows[2])
print('-----窗口3!-----')
time.sleep(1)

try:
    driver.find_element_by_xpath('//a[text()="充值购卡"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//a[text()="实体卡/卡密充值"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//a[text()="充给其他帐号"]').click()
    time.sleep(0.5)
    driver.save_screenshot('../media/login_wy.png')

    num = will_topup_number('账号')
    # num = will_topup_number('手机号')
    if '@' in num:
        print('邮箱充值')
        driver.find_element_by_id('urs_name').send_keys(num) # 账号
        driver.find_element_by_id('urs_name2').send_keys(num) # 确认账号
    else:
        print('手机号充值')
        driver.find_element_by_id('mobile').click() # 选择手机号充值
        driver.find_element_by_id('urs_mobile').send_keys(num) # 手机号
        driver.find_element_by_id('urs_mobile2').send_keys(num) # 确认手机号

    driver.find_element_by_name('cardNo').send_keys('2264001689859') # 卡号
    driver.find_element_by_name('cardPass').send_keys('839335933') # 密码
    driver.save_screenshot('../media/login_wy1.png')
    driver.find_element_by_id('charge_btn').click() # 点击充值
    time.sleep(0.5)
    driver.find_element_by_id('confirm_charge_btn').click() # 确认充值
    time.sleep(1)
    driver.save_screenshot('../media/login_wy2.png')
except Exception as e:
    print('充值出现问题')

try:
    if driver.find_element_by_xpath('//p[text()="支付失败"]').text == '支付失败':
        try:
            st = driver.find_element_by_xpath('//*[@id="fail"]/div[2]/p[2]').text
            driver.save_screenshot('../media/login_wy3.png')
            statue = {'STATUE': 400, 'MESSAGE': '支付失败', 'DATA': st}
            print(statue)
        except Exception as e:
            print(e)
    else:
        pass
        print('回调订单已启动')
except Exception as e:
    print('支付异常: ', e)

print(driver.title)
time.sleep(10)
driver.quit()
