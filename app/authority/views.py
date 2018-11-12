#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: authority/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-12 16:17:40 (CST)
# Last Update: 增加了邮件注册确认功能，当用户未点击邮件里的确认链接时，不能使用全部功能，只能显示一个未确认链接的界面
#          By:
# Description:登录注册蓝本下的路由
# **************************************************************************

from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from . import authority
from ..models import User
from ..forms import Loginform, Registerform
from ..mail import send_mail
from .. import db


@authority.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已经登录则跳转到主页面
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            # 即如果next为空或者是绝对路径
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.', 'warning')
    return render_template('authority/login.html', form=form)


@authority.route('/logout')
@login_required #我们需要注意这个修饰器的位置，位置互换会导致出错
def logout():
    logout_user()
    flash(u'您已退出登录！', 'success')
    # 注意url_for()的使用，里面参数是蓝本.视图函数的形式，可以传递参数
    return redirect(url_for('main.index'))

# 这里貌似有个情况，就是如果用户注册了账号但是发现其邮箱输错了，无法点击确认按钮的话，这种情况如何处理，此时数据库内已经有了该用户的信息，再去注册的话？
@authority.route('/register', methods=['GET', 'POST'])
def register():
    # 如果用户已经登录则跳转到主页面
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Registerform()
    if form.validate_on_submit():
        user = User(email = form.email.data.lower(), name = form.name.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirm_token()
        send_mail(user.email, '账号确认', 'authority/email/confirm', user=user, token=token)
        flash('确认邮件已经发送至您的注册邮箱，请您在10分钟内完成注册！', 'light')
        return redirect(url_for('authority.login'))#重定向到登陆页面
    return render_template('authority/register.html', form=form)


@authority.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('您已经确认了您的账户！', 'success')
    else:
        flash('您还未确认您的账号或者是该链接已经超时失效！', 'warning')
    return redirect(url_for('main.index'))

# 使用钩子来过滤用户 对于蓝本而言before_request只能应用于本蓝本之中，若想要使用全局的钩子需要使用before_app_request
# (1) 用户已登录（current_user.is_authenticated 的值为 True）。 (2) 用户的账户还未确认。 (3) 请求的 URL 不在身份验证蓝本中，而且也不是对静态文件的请求。要赋予用户访问身 份验证路由的权限，因为这些路由的作用是让用户确认账户或执行其他账户管理操作。
@authority.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'authority' and request.endpoint != 'static':
        return redirect(url_for('authority/unconfirmed'))

@authority.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or  current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('authority/unconfirmed.html')
