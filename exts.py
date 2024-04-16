#exts.py：这个文件存在的意义就是为了解决循环引用问题
#插件
#flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

#实例化对象
db = SQLAlchemy()#可以创建的时候不先绑定
mail = Mail()