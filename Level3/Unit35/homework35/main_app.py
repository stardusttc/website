from flask import Flask, redirect, render_template, session

# 【提示 5】从功能模块中导入相应的蓝图对象
# 从“翻译功能模块trans_app”中，导入蓝图对象trans_app
from trans_app import trans_app

# 从“登录注册功能模块user_app”中，导入蓝图对象user_app
from user_app import user_app

# 从“任务本功能模块todo_app”中，导入蓝图对象todo_app
from todo_app import todo_app

# 从“相册功能模块album_app”中，导入蓝图对象album_app
from album_app import album_app

# 创建Flask对象app
app = Flask(__name__)
# secret_key加密
app.secret_key = 'anbio3h4i34og'


# 【提示 6】将导入的蓝图对象注册到Flask对象app中
app.register_blueprint(trans_app)
app.register_blueprint(user_app)
app.register_blueprint(todo_app)
app.register_blueprint(album_app)



# 路由：返回欢迎页面
@app.route('/welcome')
def welcome():
    return render_template('main/welcome.html', t_my_name='壮猿')


# 路由：返回主页
@app.route('/main')
def main():
    # 获取登录的用户名
    username = session.get('username')

    # 如果获取结果为None，则表示未登录；否则，表示已登录
    if username != None:
        is_login = True
    else:
        is_login = False
        username = '游客'

    # 返回主页，将用户名和登录状态传给主页
    return render_template('main/main.html', t_username=username, t_is_login=is_login)



if __name__ == '__main__':
    # 启动web程序
    app.run(port=5001)
