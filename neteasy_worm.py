import time

from selenium import webdriver
from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_port
from values import account_number, card_number, card_password, neteasy_email_password, will_topup_number

# account_number = account_number() # 账号
# card_number = card_number()
# card_password = card_password()


class NetEasy(object):
    '''网易充值入口'''
    def __init__(self):
        # 驱动参数
        self.chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537')  # 用户中心>>软件ID 生成一个替换 96001
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-agent={}'.format(ua_pond))
        self.options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
        self.options.add_argument('--headless') # 无界面模式
        self.options.add_argument('--disable-gpu') # 隐藏gpu界面
        # self.options.add_argument('--proxy-server=http://{}'.format(ip_port()))  # ip 代理
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=self.options)
        self.url = 'https://star.game.163.com/xyq/' # 基本参数

    def login(self, acc, pwd):
        # 登陆
        time.sleep(3)
        try:
            element = self.driver.find_element_by_xpath('//a[@class="login_btn"]') # js点击登陆
            self.driver.execute_script("arguments[0].click();", element)
            print('-----登陆已经点击-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '没点击登陆 -.= ', 'DATA': e}
            return statue

        try:
            iframe = self.driver.find_element_by_xpath('//div[@id="email_login"]/iframe')  # 侧门1
            self.driver.switch_to.frame(iframe)
            t_iframe = self.driver.find_element_by_xpath('//div[@id="login-base"]/iframe')  # 侧门2
            self.driver.switch_to.frame(t_iframe)
            print('-----进门成功!-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '没进去门 -.= ', 'DATA': e}
            return statue

        try:
            self.driver.find_element_by_xpath('//div[@data-action="goEmailLogin"]').click()  # 切换句柄
            print('-----切换成功!-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '没订上 -.= ', 'DATA': e}
            return statue

        try:
            self.driver.find_element_by_xpath('//input[@data-placeholder="请输入帐号"]').clear()
            # self.driver.find_element_by_xpath('//input[@data-placeholder="请输入帐号"]').send_keys(neteasy_email_password('账号'))
            self.driver.find_element_by_xpath('//input[@data-placeholder="请输入帐号"]').send_keys(acc)
            self.driver.find_element_by_xpath('//input[@data-placeholder="请输入密码"]').clear()
            # self.driver.find_element_by_xpath('//input[@data-placeholder="请输入密码"]').send_keys(neteasy_email_password('密码'))
            self.driver.find_element_by_xpath('//input[@data-placeholder="请输入密码"]').send_keys(pwd)
            print('-----添加账号密码成功!-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '选不上东西 -.= ', 'DATA': e}
            return statue

        try:
            self.driver.find_element_by_id('dologin').click()
            print('-----登陆成功!-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '登陆失败 -.= ', 'DATA': e}
            return statue

        try:
            self.driver.switch_to.default_content()  # 退出iframe
            print('-----默认退出成功!-----')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '退出失败 -.= ', 'DATA': e}
            return statue
        
        try:
            # 切换至充值页面
            self.driver.find_element_by_xpath('//a[@title="官网"]').click()  # 跳转至官网
        except Exception as e:
            return {'STATUE':400, 'MSG':'没有切换页面'}
        
        # 1. 获取当前所有的窗口
        windows = self.driver.window_handles
        time.sleep(2)
        self.driver.switch_to.window(windows[1])
        print('-----窗口2!-----')
        self.driver.find_element_by_xpath('//a[text()="快速充值"]').click()
        time.sleep(1)
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[2])
        print('-----窗口3!-----')
        time.sleep(1)

    def parse(self, num, cn, cp):
        try:
            self.driver.find_element_by_xpath('//a[text()="充值购卡"]').click()
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//a[text()="实体卡/卡密充值"]').click()
            time.sleep(0.5)
            self.driver.find_element_by_xpath('//a[text()="充给其他帐号"]').click()
            time.sleep(0.5)
            # self.driver.save_screenshot('../media/login_wy.png')
            # num = will_topup_number('账号') # num = will_topup_number('手机号')
            if '@' in num:
                print('邮箱充值')
                self.driver.find_element_by_id('urs_name').send_keys(num)  # 账号
                self.driver.find_element_by_id('urs_name2').send_keys(num)  # 确认账号
            else:
                print('手机号充值')
                self.driver.find_element_by_id('mobile').click()  # 选择手机号充值
                self.driver.find_element_by_id('urs_mobile').send_keys(num)  # 手机号
                self.driver.find_element_by_id('urs_mobile2').send_keys(num)  # 确认手机号

            self.driver.find_element_by_name('cardNo').send_keys(cn)  # 卡号
            # self.driver.find_element_by_name('cardNo').send_keys('2264001689859')  # 卡号
            self.driver.find_element_by_name('cardPass').send_keys(cp)  # 密码
            # self.driver.find_element_by_name('cardPass').send_keys('839335933')  # 密码
            # self.driver.save_screenshot('../media/login_wy1.png')
            self.driver.find_element_by_id('charge_btn').click()  # 点击充值
            time.sleep(0.5)
            self.driver.find_element_by_id('confirm_charge_btn').click()  # 确认充值
            time.sleep(1)
            # self.driver.save_screenshot('../media/login_wy2.png')
        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '充值出现问题 -.= ', 'DATA': e}
            return statue

        try:
            if self.driver.find_element_by_xpath('//p[text()="支付失败"]').text == '支付失败':
                try:
                    st = self.driver.find_element_by_xpath('//*[@id="fail"]/div[2]/p[2]').text
                    # self.driver.save_screenshot('../media/login_wy3.png')
                    statue = {'STATUE': 400, 'MESSAGE': '支付失败', 'DATA': st}
                    return statue
                except Exception as e:
                    print(e)
            else:
                print('回调订单已启动')
                statue = {'STATUE': 200, 'MESSAGE': '支付成功', 'DATA': '成功回调参数在此'}
                return statue

        except Exception as e:
            statue = {'STATUE': 400, 'MESSAGE': '支付异常 -.= ', 'DATA': e}
            return statue

    def save(self, statue):
        # 获取充值结果
        print(statue)
        print(self.driver.title)
        time.sleep(5)
        self.driver.quit()
        return statue

    def run(self, acc, pwd, num, cn, cp):
        time.sleep(sleep_time())
        self.driver.get(self.url)  # 打开网页
        self.login(acc, pwd)
        data = self.parse(num, cn, cp)
        a = self.save(data)
        return a

# if __name__ == '__main__':
    # R = NetEasy()
    # R.run(acc, pwd, num, cn, cp)
