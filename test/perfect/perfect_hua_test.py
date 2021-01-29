import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from chaojiying_Python.chaojiying import Chaojiying_Client
from lianzhong_python.lianzhong_api import lianzhong, lianzhong_wrong
from utils import ua_pond, sleep_time, ip_pool
from values import account_number, card_number, card_password, perfect_login, choice_game_wm, choice_wm_district, \
    choice_wm_server

account_number = account_number() # 账号
card_number = card_number()
card_password = card_password()
u = choice_game_wm('诛仙3')
cwd = choice_wm_district('昊天战区')
cws = choice_wm_server('冷月笙花')

# 驱动参数
chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537') #用户中心>>软件ID 生成一个替换 96001
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(ua_pond))
options.add_argument('window-size=1920x1080') #指定浏览器分辨率
# options.add_argument('--headless') # 无界面模式
# options.add_argument('--disable-gpu') # 隐藏gpu界面
# self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)
# 基本参数
url = u
# time.sleep(sleep_time())
driver.get(url)  # 打开网页

# 充值
try:
    element = driver.find_element_by_xpath('//em[text()="完美一卡通"]')  # 点击卡密进行充值
    driver.execute_script("arguments[0].click();", element)
    print('-----登陆已经点击-----')
except Exception as e:
    statue = {'STATUE': 400, 'MESSAGE': '没点击登陆 -.= ', 'DATA': e}
    print(statue)

# 输入参数
try:
    driver.find_element_by_name('username').send_keys(account_number) # 输入账号
    driver.find_element_by_name('username2').send_keys(account_number) # 再次输入账号
except Exception as e:
    statue = {'STATUE': 400, 'MESSAGE': '卡号错误'}
    print(statue)

try:
    driver.find_element_by_name('cardnumber').send_keys(card_number) # 卡号
    driver.find_element_by_name('cardpasswd').send_keys(card_password) # 卡密
except Exception as e:
    statue = {'STATUE': 400, 'MESSAGE': '卡号或卡密错误'}
    print(statue)

time.sleep(0.5)
# 选择大区
driver.find_element_by_class_name('select').click()
driver.find_element_by_xpath(cwd)  # 选区2
try:
    element = driver.find_element_by_xpath(cws) # 选区3
    driver.execute_script("arguments[0].click();", element)
    print('-----服务器已选择-----')
except Exception as e:
    print(e)

# 截图
try:
    aa = driver.find_element_by_xpath('//div[@class="mCaptchaSlideBorder"]')
    ActionChains(driver).click_and_hold(aa).perform()
except Exception as e:
    print('点击滑块出现问题')

try:
    # 显示小滑块
    display_element = driver.find_element_by_xpath('//*[@id="captchasDivId"]/div/div[2]/div[2]/div[1]')
    driver.execute_script("arguments[0].style=arguments[1]", display_element, "display: block;")
    pic_url = driver.save_screenshot(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\perfect.png')
    print("%s:截图成功!" % pic_url)
    imgelement = driver.find_element_by_xpath('//*[@id="sliderImgContainer"]/div[1]')  # 定位验证码
    location_dict = imgelement.location  # 获取验证码x,y轴坐标
    print('lo: ', location_dict)
    # lo_location = {'x': 385, 'y': 439}
    lo_location = location_dict
    size_dict = imgelement.size  # 获取验证码的长宽
    print(size_dict)
    size = {'height': 120, 'width': 260}

    rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
              int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\perfect.png')  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    rgb_im = frame4.convert('RGB')
    rgb_im.save(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\perfect_save.png')
except Exception as e:
    print('保存失败')

try:
    # 打滑块
    json_data = lianzhong(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\perfect_save.png')
    json_data = json.loads(json_data)
    # json_data = {"data":{"val":"121,43","id":47833232020},"result":'true'}
    string = json_data['data']['val'] # 坐标
    # id
    value_id = json_data['data']['id']
    if '|' in string:
        a, b = string.split('|')
        a, c = a.split(',')
        b, d = b.split(',')

        x_offset = int(a) - int(b)
        offset = int(c) - int(d)
        # 返回值的第一个数和第三个数之差的绝对值就是要滑动的距离
        x_offset = x_offset if x_offset > 0 else -x_offset
        offset = offset if offset > 0 else -offset
        print(offset, type(offset))
        # 经过多次调试发现，如果两个坐标的y值之差大于7就会左偏 |c - d|的偏差
        if offset >= 7:
            x_offset += offset
        print(x_offset, 'if')
        # return x_offset
    else:
        # 经过多次调试发现，打码平台有时候会返回没有'|'的字符串，而此时里面的第一个数就是距离
        x_offset = string.split(',')[0]
        print(x_offset, 'else')
        # return int(x_offset)
except Exception as e:
    print('滑块请求失败')

x = int(x_offset)

try:
    # 滑动的动作链
    ActionChains(driver).click_and_hold(aa).perform()
    time.sleep(1)
    # ActionChains(driver).move_by_offset(xoffset=50, yoffset=0).perform()
    ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    # 此处一定要睡，如果不睡的话，可能还没拉到那个位置就直接进行下一步的动作了
    time.sleep(2)
    ActionChains(driver).click().perform()
except Exception as e:
    print('滑动失败')

driver.find_element_by_class_name('btn01').click() # 点击充值

try:
    # driver.find_element_by_class_name('btn05').click() # 再次确认充值
    driver.find_element_by_xpath('//*[@id="div1"]/div/center/a[1]').click() # 再次确认充值
except Exception as e:
    # lianzhong_wrong(value_id)
    print(e)

st = driver.find_element_by_class_name('other_error').text

if st == '该卡已被使用':
    statue = {'STATUE': 400, 'MESSAGE': st}
    print(statue)

print(driver.title)
time.sleep(10)
driver.quit()
