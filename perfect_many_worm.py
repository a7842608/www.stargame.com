import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from lianzhong_python.lianzhong_api import lianzhong, lianzhong_wrong
from utils import ua_pond, sleep_time, ip_port
from values import account_number, card_number, card_password, choice_game_wm, choice_wm_district, choice_wm_server

# account_number = account_number() # 账号
# card_number = card_number()
# card_password = card_password()
# u = choice_game_wm('诛仙3')
# cwd = choice_wm_district('昊天战区')
# cws = choice_wm_server('冷月笙花')


class PerfectMany(object):
    '''完美多网站充值入口'''
    def __init__(self, data):
        # 驱动参数
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent={}'.format(ua_pond))
        self.options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        self.options.add_argument('--headless') # 无界面模式
        self.options.add_argument('--disable-gpu') # 隐藏gpu界面
        # self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=self.options)
        # 基本参数
        self.url = choice_game_wm(data)

    def click(self):
        try:
            element = self.driver.find_element_by_xpath('//em[text()="完美一卡通"]')  # 点击卡密进行充值
            self.driver.execute_script("arguments[0].click();", element)
            print('-----登陆已经点击-----')
            statue = {'STATUE': 200, 'MESSAGE': '已切换至完美一通卡 -.= '}
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '没点击登陆 -.= ', 'DATA': e}
            # print(statue)
        return statue

    def input(self, an, cn, cp, dis, ser):
        # 输入参数
        try:
            # self.driver.find_element_by_name('username').send_keys(account_number)  # 输入账号
            self.driver.find_element_by_name('username').send_keys(an)  # 输入账号
            # self.driver.find_element_by_name('username2').send_keys(account_number)  # 再次输入账号
            self.driver.find_element_by_name('username2').send_keys(an)  # 再次输入账号
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '卡号错误'}
            # print(statue)
            return statue
        try:
            # self.driver.find_element_by_name('cardnumber').send_keys(card_number)  # 卡号
            self.driver.find_element_by_name('cardnumber').send_keys(cn)  # 卡号
            # self.driver.find_element_by_name('cardpasswd').send_keys(card_password)  # 卡密
            self.driver.find_element_by_name('cardpasswd').send_keys(cp)  # 卡密
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '卡号或卡密错误'}
            # print(statue)
            return statue

        time.sleep(0.5)
        # 选择大区
        self.driver.find_element_by_class_name('select').click()
        self.driver.find_element_by_xpath(choice_wm_district(dis))  # 选区2
        # self.driver.find_element_by_xpath(cwd)  # 选区2
        try:
            # element = self.driver.find_element_by_xpath(cws)  # 选区3
            element = self.driver.find_element_by_xpath(choice_wm_server(ser))  # 选区3
            self.driver.execute_script("arguments[0].click();", element)
            print('-----服务器已选择-----')
            statue = {'STATUE': 200, 'MESSAGE': '服务器已选择 -.= '}
            return statue
        except Exception as e:
            # print(e)
            return e

    def cut_img(self):
        # 截图
        try:
            aa = self.driver.find_element_by_xpath('//div[@class="mCaptchaSlideBorder"]')
            ActionChains(self.driver).click_and_hold(aa).perform()
            return aa
        except Exception as e:
            print('点击滑块出现问题')
            statue = {'STATUE': 400, 'MESSAGE': '点击滑块出现问题'}
            return statue

    def save_img(self):
        try:
            # 显示小滑块
            display_element = self.driver.find_element_by_xpath('//*[@id="captchasDivId"]/div/div[2]/div[2]/div[1]')
            self.driver.execute_script("arguments[0].style=arguments[1]", display_element, "display: block;")
            pic_url = self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/perfect.png')
            print("%s:截图成功!" % pic_url)
            imgelement = self.driver.find_element_by_xpath('//*[@id="sliderImgContainer"]/div[1]')  # 定位验证码
            location_dict = imgelement.location  # 获取验证码x,y轴坐标
            print('lo: ', location_dict)
            # lo_location = {'x': 385, 'y': 439}
            lo_location = location_dict
            size_dict = imgelement.size  # 获取验证码的长宽
            print(size_dict)
            size = {'height': 120, 'width': 260}

            rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                      int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
            i = Image.open('/www/wwwroot/www.stargame.com/media/perfect.png')  # 打开截图
            frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
            rgb_im = frame4.convert('RGB')
            rgb_im.save('/www/wwwroot/www.stargame.com/media/perfect_save.png')
        except Exception as e:
            # print('保存失败', e)
            statue = {'STATUE': 400, 'MESSAGE': '保存失败', 'DATA': e}
            return statue

    def fight_code(self, aa):
        try:
            # 打滑块
            json_data = lianzhong('/www/wwwroot/www.stargame.com/media/perfect_save.png')
            json_data = json.loads(json_data)
            # json_data = {"data":{"val":"121,43","id":47833232020},"result":'true'}
            string = json_data['data']['val']  # 坐标
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
            ActionChains(self.driver).click_and_hold(aa).perform()
            time.sleep(1)
            # ActionChains(driver).move_by_offset(xoffset=50, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
            # 此处一定要睡，如果不睡的话，可能还没拉到那个位置就直接进行下一步的动作了
            time.sleep(2)
            ActionChains(self.driver).click().perform()
        except Exception as e:
            print('滑动失败')
            return e

    def save(self):
        self.driver.find_element_by_class_name('btn01').click()  # 点击充值
        try:
            # driver.find_element_by_class_name('btn05').click() # 再次确认充值
            self.driver.find_element_by_xpath('//*[@id="div1"]/div/center/a[1]').click()  # 再次确认充值
        except Exception as e:
            # lianzhong_wrong(value_id)
            print(e)
        st = self.driver.find_element_by_class_name('other_error').text
        if st == '该卡已被使用':
            statue = {'STATUE': 400, 'MESSAGE': st}
            print(statue)
        print(self.driver.title)
        time.sleep(10)
        self.driver.quit()
        return statue
        
    def run(self, an, cn, cp, dis, ser):
        time.sleep(sleep_time())
        self.driver.get(self.url)  # 打开网页
        self.click()
        self.input(an, cn, cp, dis, ser)
        aa = self.cut_img()
        self.save_img()
        self.fight_code(aa)
        a = self.save()
        return a

# if __name__ == '__main__':
#     R = PerfectMany(data)
#     R.run(an, cn, cp, dis, ser)
