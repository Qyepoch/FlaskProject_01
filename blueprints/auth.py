import random
import string
from werkzeug.security import generate_password_hash, check_password_hash   #flask中的加密策略
from models import EmailCaptchaModel, UserModel
from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import  mail,db
from flask_mail import Message
from flask import request   #request是一个全局对象
from .forms import RegisterForm,LoginForm   #  .表示从当前目录中的forms模块中导入
# /auth
bp = Blueprint("auth",__name__,url_prefix="/auth")


@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method =='GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # #表单验证:flask-wtf: wtforms
        form = RegisterForm(request.form)#  request.form可以拿到前端form表单的数据
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=generate_password_hash(password))#密码加密存入到数据库中
            db.session.add(user)    #SQL
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 如果没有指定methods参数，默认就是get请求----
@bp.route("/login",methods=['GET','POST'])#GET请求：需要登陆页面 POST请求：提交表单
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)#得到的是一个对象
        if form.validate():         #表单数据验证成功
            # 全部验证成功
            email = form.email.data #.data 属性表示表单字段当前的值
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在")
                return redirect(url_for("auth.login"))#重定向
            if check_password_hash(user.password, password):
                #cookie:一般用来存放登录和授权你的东西
                #-----flask中的session是通过加密以后存放在cookie中的---
                session['user_id'] = user.id    # cooki里面的session
                #这行代码在登录成功之后会被放在cookie中，在以后访问其他页面的时候会被交给其他页面用来快速登录
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        # 验证失败
        else:
            print(form.errors)
            return "fail"


@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email/<email>    路径传参
    # /captcha/email?email=xxx@qq.com   查询字符串传参
    email = request.args.get("email")   #---args：参数
    # 4/6: 随机数组、宁母、数组和字母的组合
    source = string.digits*4    #随机取四位数字
    captcha = random.sample(source,4)   #---sample采样，随机采样四位
    # print(captcha)
    captcha="".join(captcha)
    # I/O操作---耗时怎么解决？多进程（message交给另外一个进程）
    message = Message(subject="知了传课验证码", recipients=[email], body=f"您的验证码是{captcha}")#主题、邮箱、右键主题
    mail.send(message)
    # memcached/redis---内存（缓存）
    # 用数据库表的方式存储---邮箱验证码（慢）
    email_captcha = EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)   #给数据库中添加对象
    db.session.commit()
    # RESTful API
    return jsonify({"code": 200,"message":"","data": None})#返回json格式--- 状态码、信息、数据

@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试",recipients=["ygl2849115967@163.com"],body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"

@bp.route("/logout")
def logout():
    session.clear()
    #清除session信息
    return redirect("/")
