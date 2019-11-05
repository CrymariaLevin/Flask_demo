# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Selvaria

from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy

'''
设计思路：
1.配置数据库，实例化数据库对象
2.添加书和作者的模型（SQLAlchemy专用）
3.添加数据（SQLAlchemy专用）
4.使用模板展示数据库查询的数据
5.使用WTF模块显示表单
6.实现相关的数据库增删改查逻辑
'''

app = Flask(__name__)
app.secret_key = "limingyiExercise1105"

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:39.105.9.20@bigdata_oil/cxd_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #动态追踪设置，建议关闭，可能已经移除了这个选项
app.config['SQLALCHEMY_ECHO'] = True #是否显示sql语句

class TestType(db.Model):
    # 定义表，
    __tablename__ = 'flask_test_type' #表名
    # 定义字段及其属性
    id = db.Column(db.INT, primary_key=True)
    author = db.Column(db.String(20), unique=True)
    #关系引用，注意这个并不是实体的列名，这个一般用于表之间一对多关系时一的一方
    # procducts是当前表用的，backref字段的'authors'是给关联的表用的，都是变量名，反向引用指到当前的表
    products = db.relationship('UnitType', backref='authors') #authors同样也是下表的虚拟列名

    def __repr__(self): #内置方法，用于打印对象的描述，否则只会返回对象的内存地址
        return "Author: %s" % self.author

class UnitType(db.Model):
    __tablename__ = 'flask_test_unit'
    id = db.Column(db.INT, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    author_id = db.Column(db.INT, db.ForeignKey('flask_test_type.id'))
    # authors = db.relationship('TestType') #关系说明部分，上边的表写过就可以了

    def __repr__(self):
        return "Product: %s, Author_id: %s" % (self.name, self.author_id)


@app.route('/', methods=['POST', 'GET'])
def index():
    url_string = 'www.google.com'
    url_list = [2, 4, 6]
    url_dict = {'name': 'test', 'index': 0}
    return render_template('comprehensive_exercise.html')

if __name__ == '__main__':
    app.run(debug=True)