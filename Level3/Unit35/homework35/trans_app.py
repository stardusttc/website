# 从flask模块中，导入蓝图Blueprint
from flask import Blueprint, render_template, request, redirect, session
import ybc_trans as trans

# 【提示 1】创建蓝图对象trans_app，名称为"trans_app"
trans_app = Blueprint('trans_app',__name__)


# 使用蓝图对象trans_app创建与“翻译功能”有关的路由

# 路由：返回翻译主页
@trans_app.route('/trans')
def index():

    username = session.get('username')
    if username == None:
        username = "游客"

    return render_template('trans/index.html', t_op='英译汉', t_username=username)


# 路由：实现翻译功能
@trans_app.route('/trans/do_trans')
def translate():

    username = session.get('username')
    if username == None:
        username = "游客"

    txt = request.args['txt']
    op = request.args['op']

    if op == '英译汉':
        result = trans.en2zh(txt)
    elif op == '汉译英':
        result = trans.zh2en(txt)

    return render_template('trans/index.html', t_txt=txt, t_result=result, t_op=op, t_username=username)
