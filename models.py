#---数据库的表
from exts import db#用SQLAlchemy连接数据库（exts是用来连接SQLAlchemy类似的插件）
from datetime import datetime
class UserModel(db.Model):#---创建用户表
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now())

class EmailCaptchaModel(db.Model):#---邮箱验证码存储
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    email = db.Column(db.String(100),nullable = False)  #邮箱
    captcha = db.Column(db.String(100),nullable = False)#验证码
    used = db.Column(db.Boolean,default=False)#验证码是否被使用

class QuestionModel(db.Model):
    __tablename__ ="question"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    #外键
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    author = db.relationship(UserModel,backref="questions")#    通过User拿到用户所有的question


class AnswerModel(db.Model):
    __tablename__="answer"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    #外键
    question_id = db.Column(db.Integer,db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    #关系
    question = db.relationship(QuestionModel,backref=db.backref("answers",order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answers")# backref：反向引用允许你从一个模型轻松访问另一个模型。