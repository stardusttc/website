# 从flask模块中，导入蓝图Blueprint
from flask import Blueprint, render_template, request, redirect, session
import pymongo
import hashlib

# 【提示 2】创建蓝图对象user_app，名称为"user_app"
user_app = Blueprint('user_app',__name__)


# 使用蓝图对象user_app创建与“用户登录注册功能”有关的路由

# 路由：访问“注册页面”
@user_app.route('/register')
def register():
    return render_template('user/register.html')


# 路由：处理注册表单，将注册用户存入数据库
@user_app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    password = request.form['password']

    user_list = find_user({'username': username})
    if len(user_list) == 0:

        pwd = encrypt(password)
        user = {'username': username, 'password': pwd}
        insert_user(user)

        # 注册成功，重定向到“登录页面”
        return redirect('/login')
    else:
        return render_template('user/register.html',
                               t_username=username,
                               t_msg='用户名已经存在')


'''
    --------与登录有关的路由--------

    /login           访问登录页面
    /login_check     处理登录表单，实现登录功能

'''


# 路由：访问“登陆页面”
@user_app.route('/login')
def login():
    return render_template('user/login.html')


# 路由：处理登录表单，实现登录功能
@user_app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']

    pwd = encrypt(password)
    user_list = find_user({'username': username, 'password': pwd})

    if len(user_list) == 1:
        # 登录成功后，将用户名存入session。该数据的键：'username'
        session['username'] = username
        # 登录成功，重定向到“主页”
        return redirect('/main')
    else:
        return render_template('user/login.html', t_error='用户名或密码错误')


# 路由：用户退出登录
@user_app.route('/logout')
def logout():
    # 删除session中的登录用户名
    session.pop('username')
    # 退出登录后，重定向到主页
    return redirect('/main')


'''
    --------与登录、注册有关的自定义函数--------

    insert_user()     将注册用户数据存入数据库
    find_user()       根据条件查找注册用户信息
    encrypt()         对密码进行加密
'''


# 函数:将注册用户数据存入数据库
def insert_user(user):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_user = client['db_user']
    c_user = db_user['user']
    c_user.insert_one(user)


# 函数：根据指定条件查找注册用户信息
def find_user(condition):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_user = client['db_user']
    c_user = db_user['user']
    res = c_user.find(condition)
    user_list = []
    for item in res:
        user_list.append(item)
    return user_list


# 使用MD5对密码进行加密
def encrypt(password):
    pwd = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    return pwd



