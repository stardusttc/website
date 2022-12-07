from flask import Flask, redirect, render_template
from monkey_app import monkey_app
from calorie_app import calorie_app
from typing_app import typing_app


# 创建Flask对象app
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(monkey_app)
app.register_blueprint(calorie_app)
app.register_blueprint(typing_app)



# 返回主页的路由
@app.route('/main')
def main():

    return render_template('main/main.html')


if __name__ == '__main__':
    app.run()
