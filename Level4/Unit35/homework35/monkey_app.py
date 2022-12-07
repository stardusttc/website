from flask import Blueprint, render_template

monkey_app = Blueprint('monkey_app',__name__)

#创建路由，路由的资源地址为'/monkey'，返回宇宙小猿页面'monkey/index.html'
@monkey_app.route('/monkey')
def index():
    return render_template('monkey/index.html')

