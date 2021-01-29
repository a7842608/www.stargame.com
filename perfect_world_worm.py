import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from chaojiying_Python.chaojiying import Chaojiying_Client
from lianzhong_python.lianzhong_api import lianzhong, lianzhong_wrong
from utils import ua_pond, sleep_time, ip_pool, ip_port
from values import account_number, card_number, card_password, perfect_login, choice_game_wm, choice_wm_district, \
    choice_wm_server

# account_number = account_number() # 账号
# card_number = card_number()
# card_password = card_password()


class PerfectWorld(object):
    '''完美点券充值入口'''
    def __init__(self):
        # 驱动参数
        self.chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537')  # 用户中心>>软件ID 生成一个替换 96001
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent={}'.format(ua_pond))
        self.options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        self.options.add_argument('--headless')  # 无界面模式
        self.options.add_argument('--disable-gpu')  # 隐藏gpu界面
        # self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=self.options)
        self.url = 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=93'

    def click(self, account, password):
        try:
            # self.driver.find_element_by_id('username').send_keys(perfect_login('账号'))
            self.driver.find_element_by_id('username').send_keys(account)
            # self.driver.find_element_by_id('passwd').send_keys(perfect_login('密码'))
            self.driver.find_element_by_id('passwd').send_keys(password)
            self.driver.find_element_by_xpath('//*[@id="wanmeiCaptcha_0"]/div/p').click()  # 点选验证码
            print('Click on the success')
        except Exception as e:
            # print('没订上', e)
            statue = {'STATUE': 404, 'MSG': '没订上', 'DATA': e}
            return statue

    def choice_fight(self):
        time.sleep(1)
        try:
            try:
                st = self.driver.find_element_by_xpath('//em[text()="依次"]').text
                print('这是点选验证码, 需要调用超级鹰', st)
                # 验证码截取参数
                self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/c_per.png')
                imgelement = self.driver.find_element_by_xpath('//img[@class="wmPicCheck-checkImg"]')  # 定位验证码
                location_dict = imgelement.location  # 获取验证码x,y轴坐标
                print('lo: ', location_dict)
                # lo_location = location_dict
                # lo_location = {'x': 295, 'y': 235} # 显示
                lo_location = {'x': 790, 'y': 330}  # 隐藏
                size_dict = imgelement.size  # 获取验证码的长宽
                print('sd: ', size_dict)
                # size = {'height': 340, 'width': 300}
                size = {'height': 400, 'width': 325}
                rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                          int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
                i = Image.open('/www/wwwroot/www.stargame.com/media/c_per.png')  # 打开截图
                frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
                rgb_im = frame4.convert('RGB')
                rgb_im.save('/www/wwwroot/www.stargame.com/media/c_per_s.png')
                # 打码
                im = open('../media/c_per_s.png', 'rb').read()
                data = self.chao_ji_ing.PostPic(im, 9004)
                try:
                    groups = data['pic_str'].split('|')
                    print(data)
                    locations = [[int(number) for number in group.split(',')] for group in groups]
                    for ii in locations:
                        ActionChains(self.driver).move_to_element_with_offset(imgelement, ii[0] - 10, ii[1] - 40).click().perform()
                        # ActionChains(driver).move_to_element_with_offset(imgelement, location[0], location[1]).click().perform()
                        time.sleep(sleep_time())
                    try:
                        self.driver.find_element_by_xpath('//a[@class="wmPicCheck-check"]').click()
                    except Exception as e:
                        # print('验证码错误', e)
                        self.chao_ji_ing.ReportError(data['pic_id'])
                        statue = {'STATUE': 400, 'MSG': '验证码错误', 'DATA': e}
                        return statue

                    time.sleep(1.5)
                    s = self.driver.find_element_by_xpath('//a[@onclick="login(event);"]')
                    self.driver.execute_script("arguments[0].click();", s)

                except Exception as e:
                    statue = {'STATUE': 404, 'MSG': '系统超时', 'DATA': e}
                    self.chao_ji_ing.ReportError(data['pic_id'])
                    return statue

            except:
                st = self.driver.find_element_by_xpath('//div[text()="向右拖动滑块完成拼图"]').text
                print('这是滑动验证码, 需要调用联众', st)
                # 截图1
                try:
                    display_element = self.driver.find_element_by_xpath('//div[@class="m_sliderBarWrapper"]')
                    ActionChains(self.driver).click_and_hold(display_element).perform()
                    time.sleep(0.5)
                    pic_url = self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/perfect1.png')
                    print("%s:截图成功!" % pic_url)
                    imgelement = self.driver.find_element_by_xpath('//div[@class="m_sliderImgShade"]')  # 定位验证码
                    location_dict = imgelement.location  # 获取验证码x,y轴坐标
                    print('lo: ', location_dict)
                    # lo_location = {'x': 315, 'y': 363} # 显示
                    lo_location = location_dict  # 隐藏
                    size_dict = imgelement.size  # 获取验证码的长宽
                    print(size_dict)
                    size = {'height': 120, 'width': 260}
                    rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                              int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
                    i = Image.open('/www/wwwroot/www.stargame.com/media/perfect1.png')  # 打开截图
                    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
                    rgb_im = frame4.convert('RGB')
                    rgb_im.save('/www/wwwroot/www.stargame.com/media/perfect_save1.png')

                    try:
                        # 打滑块
                        json_data = lianzhong('/www/wwwroot/www.stargame.com/media/perfect_save1.png')
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
                        print('滑块请求失败', e)
                        statue = {'STATUE': 400, 'MSG': '滑块请求失败', 'DATA': e}
                        lianzhong_wrong(value_id)
                        return statue

                    x = int(x_offset)
                    try:
                        # 滑动的动作链
                        ActionChains(self.driver).click_and_hold(display_element).perform()
                        time.sleep(1)
                        ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
                        time.sleep(2)  # 此处一定要睡，如果不睡的话，可能还没拉到那个位置就直接进行下一步的动作了
                        ActionChains(self.driver).click().perform()
                    except Exception as e:
                        # print('滑动失败')
                        statue = {'STATUE': 400, 'MSG': '滑动失败', 'DATA': e}
                        lianzhong_wrong(value_id)
                        return statue

                    time.sleep(1.5)
                    s = self.driver.find_element_by_xpath('//a[@onclick="login(event);"]')
                    self.driver.execute_script("arguments[0].click();", s)

                except Exception as e:
                    # print('保存失败', e)
                    statue = {'STATUE': 400, 'MSG': '保存失败', 'DATA': e}
                    return statue

        except Exception as e:
            # print('选择打码失败', e)
            statue = {'STATUE': 400, 'MSG': '选择打码失败', 'DATA': e}
            return statue

    def fight_bot(self):
        '''反机器人操作'''
        title = self.driver.title
        if title == '完美反机器人服务':
            print('被识别出来了?')
            try:
                # 点击验证
                self.driver.find_element_by_xpath('//*[@id="wanmeiCaptcha_0"]/div/p').click()
            except Exception as e:
                statue = {'STATUE': 400, 'MSG': '点击失败', 'DATA': e}
                print(statue, e)

            # 验证码截取参数
            self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/bot_fight.png')

            # 显示小滑块
            display_element = self.driver.find_element_by_xpath('//*[@id="ptCatptcha_0"]')
            self.driver.execute_script("arguments[0].style=arguments[1]", display_element, "display: block;")

            imgelement = self.driver.find_element_by_xpath('//img[@class="wmPicCheck-checkImg"]')  # 定位验证码
            location_dict = imgelement.location  # 获取验证码x,y轴坐标
            print('lo: ', location_dict)
            # lo_location = location_dict
            # lo_location = {'x': 295, 'y': 235}
            lo_location = {'x': 790, 'y': 330}  # 隐藏
            size_dict = imgelement.size  # 获取验证码的长宽
            print('sd: ', size_dict)
            size = {'height': 400, 'width': 325}
            rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                      int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
            i = Image.open('../media/bot_fight.png')  # 打开截图
            frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
            rgb_im = frame4.convert('RGB')
            rgb_im.save('/www/wwwroot/www.stargame.com/media/bot_fight.png')
            # 打码
            im = open('/www/wwwroot/www.stargame.com/media/bot_fight.png', 'rb').read()
            data = self.chao_ji_ing.PostPic(im, 9004)
            try:
                groups = data['pic_str'].split('|')
                print(data)

                locations = [[int(number) for number in group.split(',')] for group in groups]
                for ii in locations:
                    ActionChains(self.driver).move_to_element_with_offset(imgelement, ii[0] - 10,
                                                                     ii[1] - 40).click().perform()
                    # ActionChains(driver).move_to_element_with_offset(imgelement, location[0], location[1]).click().perform()
                    time.sleep(sleep_time())
                try:
                    self.driver.find_element_by_xpath('//a[@class="wmPicCheck-check"]').click()
                except Exception as e:
                    # print('验证码错误', e)
                    self.chao_ji_ing.ReportError(data['pic_id'])
                    statue = {'STATUE': 404, 'MSG': '验证码错误', 'DATA': e}
                    return statue

                time.sleep(1.5)
                s = self.driver.find_element_by_xpath('//a[@onclick="login(event);"]')
                self.driver.execute_script("arguments[0].click();", s)

            except Exception as e:
                statue = {'STATUE': 404, 'MSG': '系统超时', 'DATA': e}
                self.chao_ji_ing.ReportError(data['pic_id'])
                return statue

            self.driver.find_element_by_id('embed-submit').click()

        else:
            statue = {'STATUE': 200, 'MESSAGE': '呦呵, 通过了 -.= '}
            print(statue)
            # return statue

    def input(self, an, cn, cp):
        '''登陆后操作'''
        time.sleep(2)
        # 充值
        try:
            element = self.driver.find_element_by_xpath('//em[text()="完美一卡通"]')  # 点击卡密进行充值
            self.driver.execute_script("arguments[0].click();", element)
            print('-----登陆已经点击-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '没点击登陆 -.= ', 'DATA': e}
            # print(statue)
            return statue

        # 输入参数
        try:
            self.driver.find_element_by_name('username').clear()
            # self.driver.find_element_by_name('username').send_keys(account_number)  # 输入账号
            self.driver.find_element_by_name('username').send_keys(an)  # 输入账号
            self.driver.find_element_by_name('username2').clear()
            # self.driver.find_element_by_name('username2').send_keys(account_number)  # 再次输入账号
            self.driver.find_element_by_name('username2').send_keys(an)  # 再次输入账号
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '卡号错误', 'DATA': e}
            # print(statue)
            return statue

        try:
            # self.driver.find_element_by_name('cardnumber').send_keys(card_number)  # 卡号
            self.driver.find_element_by_name('cardnumber').send_keys(cn)  # 卡号
            # self.driver.find_element_by_name('cardpasswd').send_keys(card_password)  # 卡密
            self.driver.find_element_by_name('cardpasswd').send_keys(cp)  # 卡密
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '卡号或卡密错误', 'DATA': e}
            # print(statue)
            return statue

    def cut_img(self):
        # 截图
        try:
            aa = self.driver.find_element_by_xpath('//div[@class="mCaptchaSlideBorder"]')
            ActionChains(self.driver).click_and_hold(aa).perform()
        except Exception as e:
            # print('点击滑块出现问题')
            statue = {'STATUE': 400, 'MESSAGE': '点击滑块出现问题', 'DATA': e}
            return statue
        return aa

    def save_img(self):
        try:
            # 显示小滑块
            display_element = self.driver.find_element_by_xpath('//*[@id="captchasDivId"]/div/div[2]/div[2]/div[1]')
            self.driver.execute_script("arguments[0].style=arguments[1]", display_element, "display: block;")
            pic_url = self.driver.save_screenshot('/www/wwwroot/www.stargame.com/media/2perfect2.png')
            print("%s:截图成功!" % pic_url)
            imgelement = self.driver.find_element_by_xpath('//*[@id="sliderImgContainer"]/div[1]')  # 定位验证码
            location_dict = imgelement.location  # 获取验证码x,y轴坐标
            print('lo: ', location_dict)
            # lo_location = {'x': 385, 'y': 439} # 显示
            lo_location = location_dict  # 隐藏
            size_dict = imgelement.size  # 获取验证码的长宽
            print(size_dict)
            size = {'height': 120, 'width': 260}
            rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']),
                      int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
            i = Image.open('/www/wwwroot/www.stargame.com/media/2perfect2.png')  # 打开截图
            frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
            rgb_im = frame4.convert('RGB')
            rgb_im.save('/www/wwwroot/www.stargame.com/media/2perfect_save2.png')
        except Exception as e:
            # print('保存失败')
            statue = {'STATUE': 400, 'MESSAGE': '保存失败', 'DATA': e}
            return statue

    def fight_code(self, aa):
        t = self.driver.title
        print(t, type(t))

        if self.driver.title == '登录 - 完美世界通行证':
            print('进入失败')
        else:
            print('登陆充值界面成功!')
            try:
                # 打滑块
                json_data = lianzhong('/www/wwwroot/www.stargame.com/media/2perfect_save2.png')
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
                # print('滑块请求失败', e)
                statue = {'STATUE': 400, 'MESSAGE': '滑块请求失败', 'DATA': e}
                return statue

            try:
                x = int(x_offset)
            except Exception as e:
                lianzhong_wrong(value_id)
                # print('位置返回为空', e)
                statue = {'STATUE': 400, 'MESSAGE': '位置返回为空', 'DATA': e}
                return statue

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
            # print('滑动失败')
            statue = {'STATUE': 400, 'MESSAGE': '滑动失败', 'DATA': e}
            return statue

        try:
            self.driver.find_element_by_class_name('btn01').click()  # 点击充值
        except Exception as e:
            # print('点击失败', e)
            statue = {'STATUE': 400, 'MESSAGE': '点击失败', 'DATA': e}
            return statue

        try:
            # driver.find_element_by_class_name('btn05').click() # 再次确认充值
            self.driver.find_element_by_xpath('//*[@id="div1"]/div/center/a[1]').click()  # 再次确认充值
        except Exception as e:
            # lianzhong_wrong(value_id)
            # print(e)
            statue = {'STATUE': 400, 'MESSAGE': '二次确认充值失败', 'DATA': e}
            return statue

        st = self.driver.find_element_by_class_name('other_error').text

        if st == '该卡已被使用':
            statue = {'STATUE': 400, 'MESSAGE': st}
            # print(statue)
            return statue
            
    def save(self):
        print(self.driver.title)
        time.sleep(5)
        self.driver.quit()
        return statue

    def run(self, acc, pwd, an, cn, cp):
        time.sleep(sleep_time())
        self.driver.get(self.url)  # 打开网页
        self.click(acc, pwd)
        self.choice_fight()
        self.fight_bot()
        self.input(an, cn, cp)
        t = self.cut_img()
        self.save_img()
        a = self.fight_code(t)
        self.save()
        return a 


# if __name__ == '__main__':
#     R = PerfectWorld()
#     R.run()
