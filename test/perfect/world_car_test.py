import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool
from values import account_number, card_number, card_password, perfect_number, perfect_topup

account_number = account_number() # 账号
card_number = card_number()
card_password = card_password()

# 驱动参数
chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537') # 用户中心>>软件ID 生成一个替换 96001
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(ua_pond))
options.add_argument('window-size=1920x1080') # 指定浏览器分辨率
options.add_argument('--headless') # 无界面模式
options.add_argument('--disable-gpu') # 隐藏gpu界面
# self.options.add_argument('--proxy-server={}'.format(ip_pool))
driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)

# 基本参数
url = 'https://pay.wanmei.com/new/proxypay.do?op=prepay&gametype=200013'

# time.sleep(sleep_time())
driver.get(url)  # 打开网页

try:
    driver.find_element_by_xpath('//em[text()="完美一卡通"]').click() # 选择完美一卡通
    time.sleep(0.5)
    num = perfect_number('账号')
    driver.find_element_by_name('username').send_keys(num) # 账号
    driver.find_element_by_name('username2').send_keys(num) # 再次账号

    driver.find_element_by_name('cardnumber').send_keys(perfect_topup('卡号')) # 卡号
    driver.find_element_by_name('cardpasswd').send_keys(perfect_topup('卡密')) # 密码
except Exception as e:
    statue = {'STATUE': 400, 'MESSAGE': '账号密码无法输入'}
    print(statue)

# 选择大区
driver.find_element_by_class_name('select').click()

try:
    element = driver.find_element_by_xpath('/html/body/div[7]/dl/dd/div/a')
    driver.execute_script("arguments[0].click();", element)
    print('-----服务器已选择-----')
except Exception as e:
    print(e)

# 验证码截取参数
driver.save_screenshot(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\car_code.png')
imgelement = driver.find_element_by_id('randimg')  # 定位验证码
location_dict = imgelement.location  # 获取验证码x,y轴坐标
print('lo: ', location_dict)

# lo_location = {'x': 516, 'y': 567} # 显示
lo_location = {'x': 975, 'y': 567} # 隐式

size_dict = imgelement.size  # 获取验证码的长宽
print('hw: ', size_dict)
size = {'height': 28, 'width': 80}

rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']), int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
print('four: ', rangle)
i = Image.open(r"C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\car_code.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
rgb_im = frame4.convert('RGB')
rgb_im.save(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\car_save.png') # 保存我们接下来的验证码图片 进行打码

# 打码
im = open(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\car_save.png', 'rb').read()
data = chao_ji_ing.PostPic(im, 1005)
print(data)
if data['pic_str'] == '':
    statue = {'STATUE': 404, 'MSG': '系统超时'}
    chao_ji_ing.ReportError(data['pic_id'])
    print(statue)

code = data['pic_str']
# code = 'pgov'

try:
    driver.find_element_by_id('rand').send_keys(code) # 验证码输入
except Exception as e:
    statue = {'STATUE': 400, 'MESSAGE': '验证码输入有误'}
    chao_ji_ing.ReportError(data['pic_id'])
    print(statue)

# 提交
time.sleep(0.5)
try:
    driver.find_element_by_class_name('btn01').click()
except Exception as e:
    statue = {'STATUE': 400, 'MESSAGE': '点击失败'}
    chao_ji_ing.ReportError(data['pic_id'])
    print(statue)

time.sleep(1)
driver.find_element_by_xpath('//*[@id="div1"]/div/center/a[1]').click() # 二次确认充值

if driver.find_element_by_xpath('//div[@class="other_error"]').text == '验证码错误，请您重新输入':
    statue = {'STATUE': 400, 'MESSAGE': '验证失败'}
    chao_ji_ing.ReportError(data['pic_id'])
    print(statue)

else:
    statue = {'STATUE': 200, 'MESSAGE': '充值成功'}
    print(statue)

print(driver.title)
time.sleep(8)
driver.quit()
