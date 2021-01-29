import json
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains

from chaojiying_Python.chaojiying import Chaojiying_Client
from utils import ua_pond, sleep_time, ip_pool
from values import gh_value, account_number, card_number, card_password, choice_sever, choice_moneyclassfiy, \
    choice_sever_jw2, choice_moneyclassfiy_jw2, choice_sever_jxsj, choice_sever_jx, choice_money_jx, choice_sever_cs, \
    choice_sever_cqqz

account_number = account_number() # 账号
card_number = card_number()
card_password = card_password()

# 驱动参数
chao_ji_ing = Chaojiying_Client('nap2017', 'qweasdzxc', '909537') #用户中心>>软件ID 生成一个替换 96001
options = webdriver.ChromeOptions()
options.add_argument('--user-agent={}'.format(ua_pond))
options.add_argument('window-size=1920x1080') #指定浏览器分辨率
# options.add_argument('--headless') # 无界面模式
# options.add_argument('--disable-gpu') # 隐藏gpu界面
# self.options.add_argument('--proxy-server={}'.format(ip_pool))
driver = webdriver.Chrome('C:\\Users\\86138\\AppData\\Local\\Google\\Chrome\\Application\\chromedriver', chrome_options=options)
# 基本参数
url = 'https://charge.xoyo.com/pay?item={}&way=kcard'.format(gh_value('8'))

# time.sleep(sleep_time())
driver.get(url)  # 打开网页

# xss注入参数

if url == 'https://charge.xoyo.com/pay?item=jx3&way=kcard': # 剑网3
    # if gh_value(data) == '0':
    driver.find_element_by_id('pay_account_account').send_keys(account_number) # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number) # 确认账号
    driver.find_element_by_xpath('//input[@placeholder="请选择大区"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(choice_sever('电信一区(点月卡)')).click()
    # driver.find_element_by_xpath('//li[@id="pay_gateway_z01"]').click()
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码
    driver.find_element_by_xpath(choice_moneyclassfiy('点卡')).click()  # _6 通宝,_1月卡,_2点卡

elif url == 'https://charge.xoyo.com/pay?item=jx2&way=kcard': # 剑网2
    # elif gh_value(data) == 'jx2':
    q = choice_sever_jw2('新传区')
    driver.find_element_by_xpath(q).click()
    driver.find_element_by_xpath('//span[text()="金山一卡通支付"]').click()
    driver.find_element_by_id('pay_account_account').send_keys(account_number) # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number) # 确认账号
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码
    try:
        driver.find_element_by_xpath(choice_moneyclassfiy_jw2('大银票')).click()  # 包周/包月, 记点, 大银票
    except:
        print('你是免费区或新传区')

elif url == 'https://charge.xoyo.com/pay?item=jx2wz&way=kcard': # 剑网2外传
    # elif gh_value(data) == 'jx2wz':
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码

elif url == 'https://charge.xoyo.com/pay?item=jxsj2&way=kcard': # 剑侠世界
    # elif gh_value(data) == 'jxsj2':
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_xpath('//input[@placeholder="请选择大区"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath(choice_sever_jxsj('绿色区')).click()
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码

elif url == 'https://charge.xoyo.com/pay?item=jx&way=kcard': # 剑网1
    # elif gh_value(data) == 'jx':
    qq = choice_sever_jx('2010区')
    driver.find_element_by_xpath(qq).click()
    driver.find_element_by_xpath('//span[text()="金山一卡通支付"]').click()
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码
    try:
        driver.find_element_by_xpath(choice_money_jx('金币')).click()  # 包时, 记点, 金币
    except:
        print('你是免费区或经典区或2010')


elif url == 'https://charge.xoyo.com/pay?item=cs&way=kcard': # 反恐行动
    # elif gh_value(data) == 'cs':
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_xpath('//input[@placeholder="请选择大区"]').click()
    time.sleep(0.5)
    driver.find_element_by_id(choice_sever_cs('电信区')).click()
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码

elif url == 'https://charge.xoyo.com/pay?item=fs&way=kcard': # 封神榜 元宝区
    # elif gh_value(data) == 'fs':
    driver.find_element_by_id('undefined_fs').click()
    driver.find_element_by_xpath('//span[text()="金山一卡通支付"]').click()
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码

elif url == 'https://charge.xoyo.com/pay?item=fsib&way=kcard': # 封神榜 通宝区
    # elif gh_value(data) == 'fsib':
    driver.find_element_by_id('undefined_fsib').click()
    driver.find_element_by_xpath('//span[text()="金山一卡通支付"]').click()
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码

elif url == 'https://charge.xoyo.com/pay?item=cq&way=kcard': # 春秋Q传
    driver.find_element_by_id('pay_account_account').send_keys(account_number)  # 账号
    driver.find_element_by_id('pay_account_repeat_account').send_keys(account_number)  # 确认账号
    driver.find_element_by_xpath('//input[@placeholder="请选择大区"]').click()
    time.sleep(0.5)
    driver.find_element_by_id(choice_sever_cqqz('12-45区电信')).click()
    driver.find_element_by_id('pay_kcard_num').send_keys(card_number)  # 卡号
    driver.find_element_by_id('pay_kcard_pwd').send_keys(card_password)  # 密码

driver.execute_script('scrollTo(0,500)') # 向下滚动
time.sleep(sleep_time())
driver.find_element_by_id('create_order').click() # 立即充值
time.sleep(1.7)

'''
# 验证码截取参数
driver.save_screenshot('media/test.png') # 截取当前网页并放到E盘下命名为printscreen，该网页有我们需要的验证码
imgelement = driver.find_element_by_xpath('//div[@class="geetest_item_wrap"]/img')  # 定位验证码
location_dict = imgelement.location  # 获取验证码x,y轴坐标
# print('lo: ', location_dict)
lo_location = {'x': 784, 'y': 332}
size_dict = imgelement.size  # 获取验证码的长宽
size = {'height': 411, 'width': 335}
rangle = (int(lo_location['x']), int(lo_location['y']), int(lo_location['x'] + size['width']), int(lo_location['y'] + size['height']))  # 写成我们需要截取的位置坐标
i = Image.open("media/test.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
rgb_im = frame4.convert('RGB')
rgb_im.save('media/save.png') # 保存我们接下来的验证码图片 进行打码

# 打码
im = open('media/save.png', 'rb').read()
data = chao_ji_ing.PostPic(im, 9004)
try:
    groups = data['pic_str'].split('|')
    print(data)

    # data_dict = {'err_no': 0, 'err_str': 'OK', 'pic_id': '6002001380949200001', 'pic_str': '90,247|155,147', 'md5': '1f8e1d4bef8b11484cb1f1f34299865b'}
    # data = json.dumps(data_dict)
    # d = json.loads(data)
    # groups = d['pic_str'].split('|')

    # 点击图片上的字段 -- 156,262|84,231|189,161|249,223 报错id: 3122208545089600001
    locations = [[int(number) for number in group.split(',')] for group in groups]
    for ii in locations:
        print(ii)
        ActionChains(driver).move_to_element_with_offset(imgelement, ii[0]-10, ii[1]-40).click().perform()
        # ActionChains(driver).move_to_element_with_offset(imgelement, location[0], location[1]).click().perform()
        time.sleep(sleep_time())
    driver.save_screenshot('media/click.png')
    try:
        driver.find_element_by_xpath('//div[@class="geetest_commit_tip"]').click()

    except:
        pass
        chao_ji_ing.ReportError(data['pic_id'])

except:
    statue = {'STATUE': 404, 'MSG': '系统超时'}
    chao_ji_ing.ReportError(data['pic_id'])

time.sleep(2)
# 确认订单信息
try:
    statue = {'STATUE': 200, 'MESSAGE': 'SUCCESS'}
    driver.find_element_by_id('confirm_order_submit').click()
except:
    statue = {'STATUE': 400, 'MESSAGE': '无法确认信息, 打码失败'}
    chao_ji_ing.ReportError(data['pic_id'])
'''

# 获取充值结果
# print(statue)
print(driver.title)
time.sleep(10)
driver.quit()


