from flask import Flask, jsonify, request

# 创建服务
app = Flask(__name__)


# 指定接口的访问路径，和支持什么请求方式get，post
@app.route('/hello', methods=['get', 'post'])
def hello():
    people = request.args.get('people')
    return f"hello:\t{people}"


@app.route('/hi', methods=['get'])
def hi():
    people = request.args.get('people')
    age = request.args.get('age')
    data = {}
    data['age'] = age
    data['hi'] = people
    return jsonify(data)


if __name__ == '__main__':
    # host:指定绑定IP，port：指定绑定端口，debug指定：是否接受调试，是否返回错误信息
    app.run(host='192.168.1.104', port=8802, debug=True)
