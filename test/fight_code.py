import json
import time

# x = int(location_dict['x']) - 10
# y = int(location_dict['y']) - 520
# lo_location = {'x': x, 'y': y}
# # print(location, type(location))
# size_dict = imgelement.size  # 获取验证码的长宽
# height = int(size_dict['height']) + 70
# width = int(size_dict['width']) + 25
# size = {'height': height, 'width': width}
from collections import Counter

import cv2
from PIL import Image

# location = {'x': 304, 'y': 752}
# location = {'x': 784, 'y': 332}
# location = {'x': 799, 'y': 648}
# location = {'x': 633, 'y': 680}
# location = {'x': 618, 'y': 679}
# location = {'x': 616, 'y': 722}
# location = {'x': 1128, 'y': 680}
# location = {'x': 790, 'y': 330}
# x= +480, y= -420, h= +70, w= +35

# size = {'height': 120, 'width': 260}
# size = {'height': 400, 'width': 325}
# size = {'height': 411, 'width': 335}
# size = {'height': 26, 'width': 113}
#
location = {'x': 812, 'y': 467}
size = {'height': 120, 'width': 260}


rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
i = Image.open("../media/perfect1.png")  # 打开截图
# i = Image.open("../media/c_per.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
rgb_im = frame4.convert('RGB')
rgb_im.save('../media/perfect_test.png') # 保存我们接下来的验证码图片 进行打码
# rgb_im.save('../media/c_per_test.png') # 保存我们接下来的验证码图片 进行打码

# f = open('./save.png', 'rb')

# print(f)
# from selenium.webdriver import ActionChains
#
#
# def get_points(self, captcha_result):
#     """
#     解析识别结果
#     :param captcha_result: 识别结果
#     :return: 转化后的结果
#     """
#     groups = captcha_result.get('pic_str').split('|')
#     locations = [[int(number) for number in group.split(',')] for group in groups]
#     return locations
#
#
# def touch_click_words(self, locations):
#     """
#     点击验证图片
#     :param locations: 点击位置
#     :return: None
#     """
#     for location in locations:
#         print(location)
#         ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0],
#                                                                location[1]).click().perform()
#         time.sleep(1)

# data_dict = {'err_no': 0, 'err_str': 'OK', 'pic_id': '6002001380949200001', 'pic_str': '156,262|84,231|189,161|249,223', 'md5': '1f8e1d4bef8b11484cb1f1f34299865b'}
#
# data = json.dumps(data_dict)
#
# print(data)
# d = json.loads(data)
# # 点击图片上的字段 -- 156,262|84,231|189,161|249,223 报错id: 3122208545089600001
# groups = d['pic_str'].split('|')
# print(groups)

# from selenium import webdriver
# from utils import ua_pond, ip_port
#
# options = webdriver.ChromeOptions()
# options.add_argument('--user-agent={}'.format(ua_pond))
# options.add_argument('window-size=1920x1080') #指定浏览器分辨率
# # options.add_argument('--headless') # 无界面模式
# # options.add_argument('--disable-gpu') # 隐藏gpu界面
# options.add_argument('--proxy-server=http://{}'.format(ip_port()))
# driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)
# # 基本参数
# url = 'http://www.baidu.com'
# try:
#     driver.get(url)  # 打开网页
# except Exception as e:
#     print(e)
#
# time.sleep(3)
# print(driver.title)
# driver.quit()

# left = 10
# top = 45
# right = left + 48
# bottom = top + 52

# left = 395
# top = 485
# right = left + 48
# bottom = top + 52

# im = Image.open(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\perfect.png')
# im = Image.open(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\perfect_save.png')
# print(im.format)
# print(im.size) # (929, 889)
# print(im.mode)
# 在全屏的0截图中取出验证码的所在位置
# im = im.crop((left, top, right, bottom))

# 估计是因为屏幕的原因，从全屏截取出来的验证码的尺寸是等比例放大了的
# 但是必须用和网页中验证码的尺寸相等的图片来提交给打码平台
# 重塑图片的尺寸大小
# im = im.resize((50,50), Image.ANTIALIAS)
# im.save(r'C:\Users\86138\Desktop\2020.11.3星际游慢充\star_game\media\yan_zheng_ma.png')
