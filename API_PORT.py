# from django.http import JsonResponse
from flask import jsonify
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask_cors import CORS

from dota2_worm import DOTA2
from golden_hill_worm import GoldenHill
from neteasy_worm import NetEasy
from perfect_many_worm import PerfectMany
from perfect_world_worm import PerfectWorld
from sohu_sword_worm import SoHuWosrd
from sohu_worm import SoHu
from titan_worm import Titan
from world_car_worm import WorldCar

app = Flask(__name__)
api = Api(app)

CORS(app,  resources={r"/*": {"origins": "*"}})   # 允许所有域名跨域


class Test(Resource):
    '''测试接口'''
    def get(self):
        statue = {'Code': 200, 'Message':'接口被调用'}
        print('接口被调用')
        return statue


api.add_resource(Test, '/test')


class TitanAPIView(Resource):
    '''巨人充值选择游戏'''
    def post(self):
        an = request.form.get('account_number') # 账号
        cn = request.form.get('card_number') # 卡号
        cp = request.form.get('card_password') # 密码
        # print(an, cn, cp)
        obj = Titan()
        data = obj.run(an, cn, cp)
        return jsonify(data)


class WorldCarAPIView(Resource):
    '''创世战车'''
    def post(self):
        an = request.form.get('account_number')  # 账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)
        obj = WorldCar()
        data = obj.run(an, cn, cp)
        return jsonify(data)


class SoHuAPIView(Resource):
    '''搜狐一堆冲'''
    '''
        '3': '//a[text()="新天龙八部"]',
        '15': '//a[text()="九鼎传说"]',
        '16': '//a[text()="新水浒Ｑ传"]',
        '20': '//a[text()="鹿鼎记"]',
        '24': '//a[text()="桃园2.0"]',
        '31': '//a[text()="幻想神域"]',
        '55': '//a[text()="海战世界"]',
        '42': '//a[text()="星际战甲"]',
    '''

    def post(self):
        an = request.form.get('account_number')  # 账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        ch = request.form.get('choice_game') # 选择游戏
        # print(an, cn, cp)
        obj = SoHu(ch)
        data = obj.run(an, cn, cp)
        return jsonify(data)


class SoHuWosrdAPIView(Resource):
    '''搜狐刀剑英雄'''
    def post(self):
        an = request.form.get('account_number')  # 账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)
        obj = SoHuWosrd()
        data = obj.run(an, cn, cp)
        return jsonify(data)


class PerfectWorldAPIView(Resource):
    '''完美点券充值'''
    '''
        '账号': '18021701751',
        '密码': '888888aaA'
    '''
    def post(self):
        acc = request.form.get('game_account')  # 系统用的账号
        pwd = request.form.get('game_password')  # 系统用的密码
        an = request.form.get('account_number')  # 账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)
        obj = PerfectWorld()
        data = obj.run(acc, pwd, an, cn, cp)
        return jsonify(data)


class PerfectManyAPIView(Resource):
    '''完美一堆冲'''
    '''
    '诛仙3': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=4', # '0':
        '笑傲江湖': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=16', # '1':
        '完美世界国际版': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=3', # '2':
        '神魔大陆': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=12', # '3':
        '武林外传': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=2', # '4':
        '赤壁': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=5', # '5':
        '完美世界经典版': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=1', # '6':
        '神鬼传奇': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=11', # '7':
        '梦幻诛仙': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=8', # '8':
        '热舞派对': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=6', # '9':
        '神雕侠侣': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=19', # '10':
        '口袋西游': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=7', # '11':
        '神雕侠侣怀旧': 'https://pay.wanmei.com/new/newpay.do?op=prepay&gametype=54' # '12':
    '''
    '''
     # 诛仙3
        '变天战区': '//li[text()="变天战区"]', '幽天战区': '//li[text()="幽天战区"]', '先遣体验服': '//li[text()="先遣体验服"]',
        '昊天战区': '//li[text()="昊天战区"]', '朱天战区': '//li[text()="朱天战区"]', '炎天战区': '//li[text()="炎天战区"]',
        '玄天战区': '//li[text()="玄天战区"]', '苍天战区': '//li[text()="苍天战区"]', '钧天战区': '//li[text()="钧天战区"]',
        '阳天战区': '//li[text()="阳天战区"]',
    '''
    def post(self):
        url = request.form.get('game_choice') # 选择游戏
        dis = request.form.get('game_choice2')  # 选区2
        ser = request.form.get('game_choice3')  # 选区3
        an = request.form.get('account_number')  # 账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)

        obj = PerfectMany(url)
        data = obj.run(an, cn, cp, dis, ser)
        return jsonify(data)


class NetEasyAPIView(Resource):
    '''网易充值'''
    def post(self):
        acc = request.form.get('game_account') # 登陆账号
        pwd = request.form.get('game_password')  # 登陆密码
        num = request.form.get('account_number')  # 充值账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)
        obj = NetEasy()
        data = obj.run(acc, pwd, num, cn, cp)
        return jsonify(data)


class GoldenHillAPIView(Resource):
    '''金山充值'''
    '''
    '通宝': '//div[@id="pay_recharge_type_6"]',
        '月卡': '//div[@id="pay_recharge_type_1"]',
        '点卡': '//div[@id="pay_recharge_type_2"]',
        
        '电信一区(点月卡)': '//li[@id="pay_gateway_z01"]',
        '电信五区(点卡)': '//li[@id="pay_gateway_z05"]',
        '电信八区(点卡)': '//li[@id="pay_gateway_z08"]',
        '双线一区(点卡)': '//li[@id="pay_gateway_z21"]',
        '双线二区(点月卡)': '//li[@id="pay_gateway_z22"]',
        '双线四区(点卡)':  '//li[@id="pay_gateway_z24"]',
                     cchoice = '2'
        #     R = GoldenHill(cchoice)
        #     R.run(data, choice, an, cn, cp)
    '''
    def post(self):
        ch = request.form.get('choice_game') # 选择游戏
        data = request.form.get('choice_classfiy')  # 选择点券类型
        choice = request.form.get('choice_server')  # 选区
        an = request.form.get('account_number')  # 充值账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)
        obj = GoldenHill(ch)
        data = obj.run(data, choice, an, cn, cp)
        return jsonify(data)


class DOTA2APIView(Resource):
    '''DOTA2充值'''
    def post(self):
        an = request.form.get('account_number')  # 充值账号
        cn = request.form.get('card_number')  # 卡号
        cp = request.form.get('card_password')  # 密码
        # print(an, cn, cp)
        obj = DOTA2()
        data = obj.run(an, cn, cp)
        return jsonify(data)


'''API路由'''

api.add_resource(TitanAPIView, '/titan/post/api') # 巨人
api.add_resource(WorldCarAPIView, '/worldcar/post/api') # 创世战车
api.add_resource(SoHuAPIView, '/sohumany/post/api') # 搜狐一堆冲
api.add_resource(SoHuWosrdAPIView, '/sohuwosrd/post/api') # 搜狐刀剑英雄
api.add_resource(PerfectWorldAPIView, '/perfectworld/post/api') # 玩没点券充值
api.add_resource(PerfectManyAPIView, '/perfectmany/post/api') # 完美一堆冲
api.add_resource(NetEasyAPIView, '/neteasy/post/api') # 网易充值
api.add_resource(GoldenHillAPIView, '/goldenhill/post/api') # 金山充值
api.add_resource(DOTA2APIView, '/dota2/post/api') # DOTA2充值


if __name__ == '__main__':
    # app.run(host='192.168.0.157', port=8802, debug=True)
    # app.run(host='49.232.141.65', port=8802, debug=True)
    app.run(host='49.232.141.65', port=8802, debug=False)
    
