from flask import Blueprint, render_template

calorie_app = Blueprint('calorie_app', __name__)

#【目标1】：创建路由，路由的资源地址为'/calorie'，返回卡路里大挑战页面'calorie/index.html'
@calorie_app.route('/calorie')
def index():
    return render_template('calorie/index.html')

