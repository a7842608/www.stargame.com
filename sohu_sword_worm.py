import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool, ip_port
from values import account_number, card_number, card_password

# account_number = account_number() # 账号
# card_number = card_number()
# card_password = card_password()


class SoHuWosrd(object):
    '''搜狐刀剑英雄充值入口'''
    def __init__(self):
        # 驱动参数
        self.chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537')  # 用户中心>>软件ID 生成一个替换 96001
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent={}'.format(ua_pond))
        self.options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        self.options.add_argument('--headless')  # 无界面模式
        self.options.add_argument('--disable-gpu') # 隐藏gpu界面
        # self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=self.options)
        # 基本参数
        self.url = 'http://chong.changyou.com/djbase/cardpwdUnLoginInit.do?gameType=2'

    def parse(self, an, cn, cp):
        # xss注入参数
        # self.driver.find_element_by_id('cn').send_keys(account_number)  # 账号
        # self.driver.find_element_by_id('confirmcnId').send_keys(account_number)  # 确认账号
        # self.driver.find_element_by_id('cardNo').send_keys(card_number)  # 卡号
        # self.driver.find_element_by_id('cardPwd').send_keys(card_password)  # 密码
        self.driver.find_element_by_id('cn').send_keys(an)  # 账号
        self.driver.find_element_by_id('confirmcnId').send_keys(an)  # 确认账号
        self.driver.find_element_by_id('cardNo').send_keys(cn)  # 卡号
        self.driver.find_element_by_id('cardPwd').send_keys(cp)  # 密码

    def fight(self):
        # 验证码截取参数
        self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/sohu_sword_code.png')
        imgelement = self.driver.find_element_by_id('imageCodeId')  # 定位验证码
        location_dict = imgelement.location  # 获取验证码x,y轴坐标
        print('lo: ', location_dict)
        # lo_location = {'x': 562, 'y': 409} # {'x': 562, 'y': 409}
        lo_location = {'x': 1058, 'y': 409}  # {'x': 1058, 'y': 409} 无界面
        size_dict = imgelement.size  # 获取验证码的长宽
        print(size_dict)
        size = {'height': 26, 'width': 113}  # {'height': 26, 'width': 113}
        rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                  int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
        print(rangle)
        i = Image.open('/www/wwwroot/www.stargame.com/media/sohu_sword_code.png')  # 打开截图
        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        rgb_im = frame4.convert('RGB')
        rgb_im.save('/www/wwwroot/www.stargame.com/media/sohu_sword_save.png')  # 保存我们接下来的验证码图片 进行打码

        # 打码
        im = open('/www/wwwroot/www.stargame.com/media/sohu_sword_save.png', 'rb').read()
        data = self.chao_ji_ing.PostPic(im, 1005)
        code = data['pic_str']
        print(data)

        if data['pic_str'] == '':
            statue = {'STATUE': 404, 'MSG': '系统超时'}
            self.chao_ji_ing.ReportError(code)
            print(statue)

        self.driver.find_element_by_id('annexcode').send_keys(code)  # 验证码
        time.sleep(sleep_time())

        self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/sohu_sword_yc_code.png')  # 保存验证码后截图

        self.driver.find_element_by_xpath('//input[@value="下一步"]').click()  # 下一步

        u = self.driver.current_url  # 判断是否验证成功

        if u == 'http://chong.changyou.com/djbase/cardpwdUnLoginPay.do':
            st = self.driver.find_element_by_xpath('//span[@class="import-txt"]').text
            statue = {'STATUE': 400, 'MSG': st}
            self.chao_ji_ing.ReportError(code)
            # print(statue)
            return statue

        else:
            print('充值成功')
            pass

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
#     R = SoHuWosrd()
#     R.run()
