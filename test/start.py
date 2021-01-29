from flask import Flask, Blueprint
from flask_restful import Api, Resource
from API_PORT import Test

app = Flask(__name__)
api = Api(app)

'''url'''
api.add_resource(Test, '/test') # 测试


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8802, debug=True)