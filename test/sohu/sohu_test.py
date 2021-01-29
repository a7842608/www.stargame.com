import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool
from values import account_number, card_number, card_password, choice_sever_SOHU

account_number = account_number() # 账号
card_number = card_number()
card_password = card_password()

# 驱动参数
chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537') #用户中心>>软件ID 生成一个替换 96001
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(ua_pond))
options.add_argument('window-size=1920x1080') #指定浏览器分辨率
options.add_argument('--headless') # 无界面模式
# options.add_argument('--disable-gpu') # 隐藏gpu界面
# self.options.add_argument('--proxy-server={}'.format(ip_pool))
driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)
# 基本参数
url = 'http://chong.changyou.com/'

# time.sleep(sleep_time())
driver.get(url)  # 打开网页

# # xss注入参数
driver.find_element_by_xpath('//a[@class="normal fast_payBtn"]').click() # 点击快速充值
driver.find_element_by_xpath('//input[@name="cn"]').send_keys(account_number) # 账号
driver.find_element_by_xpath('//input[@name="cn2"]').send_keys(account_number) # 确认账号
driver.find_element_by_xpath('//input[@name="cardNo"]').send_keys(card_number)  # 卡号
driver.find_element_by_xpath('//input[@name="cardPwd"]').send_keys(card_password)  # 密码
time.sleep(sleep_time())
# 选择游戏
driver.find_element_by_xpath('//*[@id="fast_pay_ul"]/li[4]/div').click() # 1
choice_game = choice_sever_SOHU('55')
driver.find_element_by_xpath(choice_game).click() # 2
# 选择大区
try:
    driver.find_element_by_xpath('//*[@id="dlgame_select_rid"]/div').click() # 选择大区1
    if choice_game == '//a[text()="幻想神域"]': # 31
        driver.find_element_by_xpath('//a[text()="一区-启源大陆"]').click() # 选择大区2
    elif choice_game == '//a[text()="海战世界"]': # 55
        driver.find_element_by_xpath('//a[text()="中途岛（双线区）"]').click() # 选择大区2
    elif choice_game == '//a[text()="星际战甲"]': # 42
        driver.find_element_by_xpath('//*[@id="dlgame_region_id_box"]/a').click() # 选择大区2

except:
    print('你选的是前五个')

time.sleep(sleep_time())


# 验证码截取参数
driver.save_screenshot('../media/sohu_code.png')
imgelement = driver.find_element_by_id('checkcodeId')  # 定位验证码
location_dict = imgelement.location  # 获取验证码x,y轴坐标
print('lo: ', location_dict)

if choice_game == '//a[text()="幻想神域"]':
    print('幻想神域')
    lo_location = {'x': 1128, 'y': 722}
    # lo_location = {'x': 616, 'y': 722}
elif choice_game == '//a[text()="海战世界"]':
    print('海战世界')
    lo_location = {'x': 1128, 'y': 722}
    # lo_location = {'x': 616, 'y': 722}
elif choice_game == '//a[text()="星际战甲"]':
    print('星际战甲')
    lo_location = {'x': 1128, 'y': 722}
    # lo_location = {'x': 616, 'y': 722}
else:
    print('前五个')
    lo_location = {'x': 1128, 'y': 680}
    # lo_location = {'x': 618, 'y': 679}

size_dict = imgelement.size  # 获取验证码的长宽
print(size_dict)
size = {'height': 33, 'width': 91}

rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']), int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
print(rangle)
i = Image.open("../media/sohu_code.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
rgb_im = frame4.convert('RGB')
rgb_im.save('../media/sohu_save.png') # 保存我们接下来的验证码图片 进行打码

# 打码
im = open('../media/sohu_save.png', 'rb').read()
data = chao_ji_ing.PostPic(im, 1005)
print(data)
if data['pic_str'] == '':
    statue = {'STATUE': 404, 'MSG': '系统超时'}
    chao_ji_ing.ReportError(data['pic_id'])
    print(statue)

# data_dict = {'err_no': 0, 'err_str': 'OK', 'pic_id': '9122415085089600039', 'pic_str': 'RNCZM', 'md5': '22fda2e7d516a448c271486dc35f32f0'}
# code = data_dict['pic_str']
# if data_dict['pic_str'] == '':
#     statue = {'STATUE': 404, 'MSG': '系统超时'}
#     chao_ji_ing.ReportError(data['pic_id'])

code = data['pic_str']
driver.find_element_by_id('annexcode').send_keys(code)  # 验证码
time.sleep(sleep_time())
driver.save_screenshot('../media/sohu_yc_code.png') # 保存验证码后截图
driver.find_element_by_xpath('//a[text()="充值"]').click() # 立即充值
st = driver.find_element_by_xpath('//p[@id="error"]').text
if st == '呦！您输入的验证码不正确呀':
    statue = {'STATUE': 400, 'MESSAGE': '验证码错误, 打码失败'}
    chao_ji_ing.ReportError(data['pic_id'])
    print(statue)
else:
    statue = {'STATUE': 200, 'MESSAGE': 'SUCCESS'}
    # 确认订单信息
    # 获取充值结果
    print(statue)
    print(driver.title)
time.sleep(10)
driver.quit()
