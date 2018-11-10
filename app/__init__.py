#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: __init__.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 15:34:50 (CST)
# Last Update: 2018-11-10 16:40:34 (CST) 将主蓝本注册到工厂处理函数中
#          By:
# Description:工厂处理函数 create_app
# **************************************************************************

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config #导入的即congfig.py中的数据字典

#导入使用的应用扩展，由于应用实例还未创建所以在这里创建扩展类的时候并没有向构造函数传入参数
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()


def create_app(config_name):
    #需注意create_app方法中的参数config_name在使用时要使用config配置文件中数据字典中的值，从而达到使用不同配置选项的目的
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    #在此处添加路由
    from .main_blue import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
