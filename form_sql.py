# !/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Selvaria
# 使用pymysql连接数据库

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo
import pymysql
from resources.base import BaseDb

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
    a.在网页实现删除数据的话，点击需要发送请求给指定的路由--》路由的路径需要接收参数
    flask后台中redirect，url_for的使用，网页HTML中url_for，控制代码块for else的使用
'''

app = Flask(__name__)
app.secret_key = "limingyiExercise1105"

bd = BaseDb()

#表单类
class TestForm(FlaskForm):
    author = StringField(label='作者：', validators=([DataRequired(),]))
    product = StringField('作品：', validators=([DataRequired()]))
    submit = SubmitField('提交')

@app.route('/pymysql_form', methods=['POST', 'GET'])
def pymysql_index():
    # 将自定义表单类内容传递给模板
    form = TestForm()

    # 提交数据至数据库，并进行相关验证
    if form.validate_on_submit(): #其实就是在验证表单类的各个验证函数
        # author = request.form.get('作者')
        # product = request.form.get('作品')
        # 注意下面这种数据获取方式
        author = form.author.data
        product = form.product.data

        author_sql = "select * from `flask_test_type` where author='{}'".format(author)
        bd.dict_cur.execute(author_sql)
        author_dict = bd.dict_cur.fetchone()
        if not author_dict:
            try:
                author_new = "INSERT INTO `flask_test_type` (`author`) VALUES ('{}')".format(author)
                bd.dict_cur.execute(author_new)
                bd.conn.commit()
                print('添加作者成功')

                author_add_sql = "select * from `flask_test_type` where author='{}'".format(author)
                bd.dict_cur.execute(author_add_sql)
                author_add_dict = bd.dict_cur.fetchone()
                product_new = "INSERT INTO `flask_test_unit` (`name`, `author_id`) VALUES ('{0}', '{1}')".format(product, author_add_dict['id'])
                bd.dict_cur.execute(product_new)
                bd.conn.commit()
                flash('添加作者及其书籍成功')
            except Exception as e:
                print(str(e))
                flash('添加作者及其书籍失败')
                bd.conn.rollback()  # 数据库已完成的操作全部撤销
        else:
            author_id_sql = "select * from `flask_test_type` where author='{}'".format(author)
            bd.dict_cur.execute(author_id_sql)
            author_id_dict = bd.dict_cur.fetchone()
            author_id = author_id_dict.get('id')

            product_sql = "select * from `flask_test_unit` where `name`='{}'".format(product)
            bd.dict_cur.execute(product_sql)
            product_id_dict = bd.dict_cur.fetchone()
            if not product_id_dict:
                try:
                    product_new = "INSERT INTO `flask_test_unit` (`name`, `author_id`) VALUES ('{0}', '{1}')".format(product, author_id)
                    bd.dict_cur.execute(product_new)
                    bd.conn.commit()
                    flash('添加书籍成功')
                except Exception as e:
                    print(str(e))
                    flash('添加书籍失败')
                    bd.conn.rollback() #数据库已完成的操作全部撤销
            else:
                flash('已存在同名书籍')
    else:
        if request.method == 'POST':
            flash('参数有误')

    # 查询作者信息，数据库内容传递给模板
    authors = "select * from `flask_test_type`"
    bd.dict_cur.execute(authors)
    author_dict = bd.dict_cur.fetchall()
    # print(author_dict)
    products = "select * from `flask_test_unit`"
    bd.dict_cur.execute(products)
    product_dict = bd.dict_cur.fetchall()
    # print(product_dict)
    # product_list = []
    # for author in authors:
    #     product_single = "select * from `flask_test_unit` where `author_id`='{}'".format(author)
    #     bd.dict_cur.execute(product_single)
    #     product_dict = bd.dict_cur.fetchall()
    #     product_list.append(product_dict)

    return render_template('pymysql_html.html', author_h5=author_dict, product_h5=product_dict, form_h5=form)

@app.route('/delete_product/<product_id>', methods=['POST', 'GET'])
def delete_product(product_id):
    # 先验证是否有该id，没有提示错误
    p_result = "select * from `flask_test_unit` where `id`='{}'".format(product_id)
    if p_result:
        try:
            product_del = "DELETE FROM `flask_test_unit` WHERE `id` = '{}'".format(product_id)
            bd.dict_cur.execute(product_del)
            bd.conn.commit()
        except Exception as e:
            print(str(e))
            flash('删除作品失败')
            bd.conn.rollback()
    else:
        flash('没有该作品')
    return redirect(url_for('pymysql_index'))  # 传入视图函数名，返回该视图函数对应的路由地址

@app.route('/delete_author/<author_id>', methods=['POST', 'GET'])
def delete_author(author_id):
    # 先验证是否有该id，没有提示错误
    a_sql = "select * from `flask_test_type` where `id`='{}'".format(author_id)
    bd.dict_cur.execute(a_sql)
    a_result = bd.dict_cur.fetchone()
    # print(a_result)
    # a_tuple = str(tuple(a_result))
    if a_result:
        try:
            # 注意要先删书
            product_del = "DELETE FROM `flask_test_unit` WHERE `author_id` = {}".format(author_id)
            bd.dict_cur.execute(product_del)
            bd.conn.commit()
            author_del = "DELETE FROM `flask_test_type` WHERE `id` = {}".format(author_id)
            bd.dict_cur.execute(author_del)
            bd.conn.commit()
        except Exception as e:
            print(str(e))
            flash('删除作者失败')
            bd.conn.rollback()
    else:
        flash('没有该作者')
    return redirect(url_for('pymysql_index')) #传入视图函数名，返回该视图函数对应的路由地址

if __name__ == '__main__':
    app.run(debug=True)