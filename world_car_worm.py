import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_port
from values import account_number, card_number, card_password, perfect_number, perfect_topup

# account_number = account_number() # 账号
# card_number = card_number()
# card_password = card_password()


class WorldCar(object):
    '''创世战车充值入口'''
    def __init__(self):
        # 驱动参数
        self.chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537')  # 用户中心>>软件ID 生成一个替换 96001
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent={}'.format(ua_pond))
        self.options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        self.options.add_argument('--headless')  # 无界面模式
        self.options.add_argument('--disable-gpu')  # 隐藏gpu界面
        self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=self.options)
        # 基本参数
        self.url = 'https://pay.wanmei.com/new/proxypay.do?op=prepay&gametype=200013'

    # def parse(self):
    def parse(self, an, cn, cp):
        try:
            self.driver.find_element_by_xpath('//em[text()="完美一卡通"]').click()  # 选择完美一卡通
            time.sleep(0.5)
            num = perfect_number('账号')
            # self.driver.find_element_by_name('username').send_keys(num)  # 账号
            self.driver.find_element_by_name('username').send_keys(an)  # 账号
            # self.driver.find_element_by_name('username2').send_keys(num)  # 再次账号
            self.driver.find_element_by_name('username2').send_keys(an)  # 再次账号

            # self.driver.find_element_by_name('cardnumber').send_keys(perfect_topup('卡号'))  # 卡号
            self.driver.find_element_by_name('cardnumber').send_keys(cn)  # 卡号
            self.driver.find_element_by_name('cardpasswd').send_keys(cp)  # 密码
            # self.driver.find_element_by_name('cardpasswd').send_keys(perfect_topup('卡密'))  # 密码
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '账号密码无法输入'}
            print(statue)

        # 选择大区
        self.driver.find_element_by_class_name('select').click()

        try:
            element = self.driver.find_element_by_xpath('/html/body/div[7]/dl/dd/div/a')
            self.driver.execute_script("arguments[0].click();", element)
            print('-----服务器已选择-----')
        except Exception as e:
            print(e)

    def fight(self):
        # 验证码截取参数
        self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/car_code.png')
        imgelement = self.driver.find_element_by_id('randimg')  # 定位验证码
        location_dict = imgelement.location  # 获取验证码x,y轴坐标
        print('lo: ', location_dict)

        # lo_location = {'x': 516, 'y': 567} # 显示
        lo_location = {'x': 975, 'y': 567}  # 隐式

        size_dict = imgelement.size  # 获取验证码的长宽
        print('hw: ', size_dict)
        size = {'height': 28, 'width': 80}

        rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                  int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
        print('four: ', rangle)
        i = Image.open("/www/wwwroot/www.stargame.com/media/car_code.png")  # 打开截图
        frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
        rgb_im = frame4.convert('RGB')
        rgb_im.save('/www/wwwroot/www.stargame.com/media/car_save.png')  # 保存我们接下来的验证码图片 进行打码

        # 打码
        im = open('/www/wwwroot/www.stargame.com/media/car_save.png', 'rb').read()
        data = self.chao_ji_ing.PostPic(im, 1005)
        print(data)
        if data['pic_str'] == '':
            statue = {'STATUE': 404, 'MSG': '系统超时'}
            self.chao_ji_ing.ReportError(data['pic_id'])
            # print(statue)
            return statue

        code = data['pic_str']
        # code = 'pgov'

        try:
            self.driver.find_element_by_id('rand').send_keys(code)  # 验证码输入
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '验证码输入有误'}
            self.chao_ji_ing.ReportError(data['pic_id'])
            # print(statue)
            return statue

        # 提交
        time.sleep(0.5)
        try:
            self.driver.find_element_by_class_name('btn01').click()
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '点击失败'}
            self.chao_ji_ing.ReportError(data['pic_id'])
            # print(statue)
            return statue

        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="div1"]/div/center/a[1]').click()  # 二次确认充值

        if self.driver.find_element_by_xpath('//div[@class="other_error"]').text == '验证码错误，请您重新输入':
            statue = {'STATUE': 400, 'MESSAGE': '验证失败'}
            self.chao_ji_ing.ReportError(data['pic_id'])
            # print(statue)
            return statue

        else:
            statue = {'STATUE': 200, 'MESSAGE': '充值成功'}
            # self.chao_ji_ing.ReportError(data['pic_id'])
            # print(statue)
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
    # R = WorldCar()
    # R.run()
