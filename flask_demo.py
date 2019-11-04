# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Selvaria

# render_template用于返回网页;
# request是请求对象，可以获取请求方式
# flash是动态传递消息模块，给模板传递消息，模板中要遍历所有的flash消息，需要设置secret_key用于加密
from flask import Flask, render_template, request, flash

from flask_wtf import FlaskForm # 表单类
from wtforms import SubmitField, StringField, PasswordField #自定义表单需要的字段
from wtforms.validators import DataRequired, EqualTo #wtf扩展提供的表单验证器。DataRequired表示必填，EqualTo表示两者要相同
import pymysql

from flask_sqlalchemy import SQLAlchemy #数据库模块

app = Flask(__name__) # Flask实例需要传入项目名字，"__name__"必须写
app.secret_key = "lisadfsdfminhkggdfsyi" #flash用加密信息，用于混淆

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://root:580225@127.0.0.1/flask_demo_sql'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #动态追踪设置，建议关闭，可能已经移除了这个选项
app.config['SQLALCHEMY_ECHO'] = True #是否显示sql语句

#数据库的模型，这里是建表
class Role(db.Model): #角色分类表
    # 定义表，
    __tablename__ = 'roles'
    # 定义字段及其属性
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(20), unique=True)

class User(db.Model): #用户表
    __tablename__ = 'users'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(20))
    type_num = db.Column(db.INT, db.ForeignKey('roles.id')) #标明是外键，关联到roles表的id


# 新建表单验证类，这个是flask对应刀html语言的设置类，目前暂时不建议使用
class RegisterForm(FlaskForm):
    username = StringField('用户：', validators=[DataRequired()])
    password = PasswordField('密码：', validators=[DataRequired()])
    password2 = PasswordField('确认密码：', validators=[DataRequired(), EqualTo('password', message='Passwords must be same')])
    submit = SubmitField('提交')


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

#利用flask_WTF模块构建表单，不好用，而且前后端不易分离
@app.route('/formwtf', methods=['POST', 'GET'])
def form_wtf():
    rf = RegisterForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print(username, password, password2)
        #验证方式
        if rf.validate_on_submit(): #提交的时候会执行验证函数
            return 'Success'
        else:
            flash('参数有误')

    return render_template('form_wtf.html', form=rf)



# 删除表，实际开发基本不会使用
db.drop_all()
# 创建表，实际开发基本不会使用
db.create_all()

if __name__ == '__main__':

    #增加行：
    role1 = Role(name='admin')
    db.session.add(role1)
    db.session.commit()
    user1 = User(name='Xiaoming', type_num=role1.id)
    db.session.add(user1)
    db.session.commit()
    # 修改行
    user1.name = 'Xiaoxiaoming'
    db.session.commit()
    # 删除行
    db.session.delete(user1)
    db.session.commit()
    # 运行起一个简易服务器
    app.run(debug=True) #此时不用手动重新运行程序，在网页刷新即可
