# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Selvaria

# render_template用于返回网页;
# request是请求对象，可以获取请求方式
# flash是动态传递消息模块，给模板传递消息，模板中要遍历所有的flash消息，需要设置secret_key用于加密
from flask import Flask, render_template, request, flash

app = Flask(__name__) # Flask实例需要传入项目名字，"__name__"必须写
app.secret_key = "lisadfsdfminhkggdfsyi" #flash用加密信息，用于混淆

@app.route('/', methods=['POST', 'GET']) # 定义路由，flask中是通过装饰器实现，默认只有get方法
def hello_world(): #视图函数
    return 'Hello Flask!'

# 使用同一个视图函数，显示不同的订单（页面）信息
@app.route('/orders/<order_id>', methods=['POST', 'GET']) # 注意在路径里用<>表示动态信息
# @app.route('/orders/<int: order_id>', methods=['POST', 'GET']) #注意这里限定了order_id的类型
def get_order(order_id):
    # 需要在函数内传入参数，且要和路径的参数名一致
    return 'order_id: %s' % order_id

# 返回一个网页
@app.route('/index', methods=['POST', 'GET'])
def index():
    url_string = 'www.google.com'
    url_list = [2, 4, 6]
    url_dict = {'name': 'test', 'index': 0}
    return render_template('index.html',  #这里是向网页中传入参数，注意html文件的写法
                           url=url_string,
                           t_list=url_list,
                           t_dict=url_dict
                           )
    # 正常第一个参数之后的参数都是键值对，用于向网页传入参数

# 表单相关数据设计
@app.route('/form', methods=['POST', 'GET'])
def form_handle():
    if request.method == 'POST': #判断请求方式
        # 获取表单的参数
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # flash([username, password, password2])
        print(username, password, password2)
        if not all([username, password, password2]):
            #return  'All forms must be filled'
            flash('All forms must be filled') #如果中文可以在字符前加u，如：flash(u'都填上')
        elif password != password2:
            flash('Passwords must be same')
            # return 'Passwords must be same'
        else:
            return 'Success'
    return render_template('form.html')

if __name__ == '__main__':
    # 运行起一个简易服务器
    app.run(debug=True) #此时不用手动重新运行程序，在网页刷新即可
