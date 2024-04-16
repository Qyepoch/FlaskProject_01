from functools import wraps

from flask import g, redirect, url_for

# 装饰器函数：装饰器是一种在不修改函数的情况下，动态修改函数行为的手段，可以在不修改原有函数的前提下添加附加功能。
def login_required(func):
    #保func的信息 wrap:包裹
    @wraps (func)# falsk程序中不能少
    def inner(*args,**kwargs):
        if g.user:
            #第一个用来接收任意数量的--位置参数--，第二个用来接收任意数量的--关键字参数--
            return func(*args, **kwargs)# * 表示位置参数 **表示关键字参数(1,2,c = 3) 1,2是位置参数 c = 3 是关键字参数
        else:
            return redirect(url_for("auth.login"))
    return inner
    # 需要 return inner 才能替换原有的函数，让装饰器生效。如果不 return inner，原有的函数 func 将无法被装饰器修改，装饰器将不起作用。
        # @login_required
        # def public_question(quesiton_id):
        #   pass
        # login_required(public_question)(question_id)f
'''
inner 函数是装饰器函数，它接收一个函数 func 作为参数，并返回一个新的函数。这个新的函数将执行以下操作：

检查用户是否已登录：如果用户已登录，则调用原始函数 func 并返回其返回值。
如果用户未登录，则将用户重定向到登录页面。
这样，当使用 @login_required 装饰器装饰一个函数时，如果用户未登录，系统会自动将用户重定向到登录页面，而无需在函数内部显式检查登录状态。
'''