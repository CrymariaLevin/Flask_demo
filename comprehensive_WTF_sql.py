# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Selvaria

from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo
from flask_sqlalchemy import SQLAlchemy
import pymysql

'''
设计思路：
1.配置数据库，实例化数据库对象
2.添加书和作者的模型（SQLAlchemy专用）
3.添加数据（SQLAlchemy专用）
4.使用模板展示数据库查询的数据
5.使用WTF模块显示表单
    a.自定义表单类
    b.设置secret_key 以及解决编码问题，csrf_token设置问题
6.实现相关的数据库增删改查逻辑
'''

app = Flask(__name__)
app.secret_key = "limingyiExercise1105"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:bigdata_oil@39.105.9.20:3306/cxd_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #动态追踪设置，建议关闭，可能已经移除了这个选项
app.config['SQLALCHEMY_ECHO'] = True #是否显示sql语句

db = SQLAlchemy(app) #一定要放在参数设置的后面

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

#表单类
class TestForm(FlaskForm):
    author = StringField(label='作者：', validators=([DataRequired(),]))
    product = StringField('作品：', validators=([DataRequired()]))
    submit = SubmitField('提交')

@app.route('/', methods=['POST', 'GET'])
def index():
    # 将自定义表单类内容传递给模板
    form = TestForm()

    # 提交数据至数据库，并进行相关验证
    if form.validate_on_submit(): #其实就是在验证表单类的各个验证函数
        # author = request.form.get('作者')
        # product = request.form.get('作品')
        # 注意下面这种数据获取方式
        author = form.author.data
        product = form.product.data

        author_sql = TestType.query.filter_by(author=author).first()
        if not author_sql:
            author_new = TestType(author=author)
            product_new = UnitType(name=product)
            db.session.add([author_new, product_new])
            db.session.commit()
        else:
            product_sql = UnitType.query.filter_by(name=product).first()
            if not product_sql:
                try:
                    product_new = UnitType(name=product, author_id=author_sql.id)
                    db.session.add(product_new)
                    db.session.commit()
                except Exception as e:
                    print(str(e))
                    flash('添加书籍失败')
                    db.session.rollback() #数据库已完成的操作全部撤销
            else:
                flash('已存在同名书籍')
    else:
        if request.method == 'POST':
            flash('参数有误')

    # 查询作者信息，数据库内容传递给模板
    authors = TestType.query.all()
    #print(type(authors))
    #print(authors)
    return render_template('comprehensive_exercise.html', author_h5=authors, form_h5=form)

if __name__ == '__main__':
    app.run(debug=True)