# 表单验证模块
import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db

# Form：主要就是验证前端的表单数据是否符合要求
class RegisterForm(wtforms.Form):#继承
    #Stringfiled：字符串类型
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误!")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次输入密码不一致")])

    # 自定义验证方法---> validate_XXX
    def validate_email(self, field):
        """检查邮箱是否已经被注册"""
        email = field.data
        user = UserModel.query.filter_by(email=email).first()#从数据库中检索
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册!")#验证错误
        #默认验证成功

    def validate_captcha(self, field):#self代表当前对象
        """检查验证码是否正确"""
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误!")
            # DONE: 可以删除 captcha_model
        else:
            db.session.delete(captcha_model)#验证码失效（被用过）
            db.session.commit()

class LoginForm(wtforms.Form):
    email= wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误!")])

class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误!")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误!")])

class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误!")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id!")])