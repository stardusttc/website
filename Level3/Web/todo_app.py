# 从flask模块中，导入蓝图Blueprint
from flask import Blueprint, render_template, request, session, redirect
import pymongo
import datetime
import uuid

# 【提示 3】创建蓝图对象todo_app，名称为"todo_app"
todo_app = Blueprint('todo_app',__name__)


# 使用蓝图对象todo_app创建与“任务本功能”有关的路由

# 路由：访问“任务列表页面”，实现查询功能
@todo_app.route('/todo')
def list_page():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')


    # 创建数据库查询条件
    condition = {}
    condition['owner'] = username

    # 1、获取提交的date和subject
    date = request.args.get('date')
    subject = request.args.get('subject')

    # 2、将date添加到查询条件condition
    if date == None:
        date = '全部'
    elif date == '今天':
        condition['date'] = str_today()
    elif date == '昨天':
        condition['date'] = str_yesterday()

    # 3、将subject添加到查询条件condition
    if subject == None:
        subject = '全部'
    elif subject != '全部':
        condition['subject'] = subject

    # 在控制台输出条件
    print(condition)

    # 使用find_todo()函数查询符合条件的任务数据
    todo_list = find_todo(condition)

    # 使用查询到的任务列表渲染页面
    date_options = ['全部', '今天', '昨天']
    subject_options = ['全部', '语文', '数学', '英语', '编程']

    return render_template('todo/list.html',
                           t_username=username,
                           t_todo_list=todo_list,
                           t_date_options=date_options,
                           t_subject_options=subject_options,
                           t_date=date,
                           t_subject=subject)


# 路由：返回“添加任务页面”
@todo_app.route('/todo/add')
def todo_add():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')


    # 获取今天的日期字符串
    today = str_today()

    # 创建任务时的可选科目
    subjects = ['语文', '数学', '英语', '编程']
    return render_template('todo/todo_add.html',
                           t_subject_options=subjects,
                           t_date=today,
                           t_username=username)


# 路由：获取添加任务表单提交的数据，实现添加任务功能
@todo_app.route('/add_check', methods=['POST'])
def add_check():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')


    # 创建存储任务数据的字典
    todo = {}

    # 获取表单提交的任务数据subject、content，并将数据添加到字典todo中
    todo['subject'] = request.form.get('subject')
    todo['content'] = request.form.get('content')

    # 向字典todo中添加_id、state、owner、date
    todo['date'] = str_today()
    todo['_id'] = str(uuid.uuid1())
    todo['state'] = 'unfinished'
    todo['owner'] = username

    # 将存储任务信息的字典存入数据库
    insert_todo(todo)

    # 重定向到任务本主页
    return redirect('/todo')


# 路由：实现将任务设置为“已完成”
@todo_app.route('/todo/finished')
def todo_finish():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')


    # 获取任务的_id，将该任务的状态修改为“已完成”
    id_str = request.args.get('_id')
    if id_str != None:
        finish_todo(id_str)

    # 重定向到任务列表页面
    return redirect('/todo')


# 路由：实现将任务设置为“未完成”
@todo_app.route('/todo/unfinished')
def todo_unfinish():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')


    # 获取任务的_id，将该任务的状态修改为“未完成”
    id_str = request.args.get('_id')
    if id_str != None:
        unfinish_todo(id_str)

    # 重定向到任务列表页面
    return redirect('/todo')


# 路由：实现删除任务，即将任务状态改为“已删除”
@todo_app.route('/todo/deleted')
def todo_delete():
    # 访问控制：如果没有登录，则重定向到登录页面
    username = session.get('username')
    if username == None:
        return redirect('/login')

    # 获取将要被删除任务的_id，将该任务的状态修改为“已删除”
    id_str = request.args.get('_id')

    if id_str != None:
        delete_todo(id_str)

    # 重定向到任务列表页面
    return redirect('/todo')


'''
    --------与任务本有关的自定义函数--------

    insert_todo()      存储新的任务
    find_todo()        根据条件查询任务
    finish_todo()      将任务状态改为“已完成”
    unfinish_todo()    将任务状态改为“未完成”
    delete_todo()      将任务状态改为“已删除”，即删除任务
    str_today()        获取今天的日期(字符串)
    str_yesterday()    获取昨天的日期(字符串)

'''


# 函数：存储新的任务
def insert_todo(todo):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    c_todo.insert_one(todo)


# 函数：根据条件查询任务
def find_todo(condition):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    res = c_todo.find(condition)
    todo_list = []
    for item in res:
        todo_list.append(item)
    return todo_list


# 函数：根据任务的_id，将任务状态更新为“已完成”
def finish_todo(todo_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    # 先根据_id查询到任务，再更新任务状态“state”
    todo = c_todo.find_one({'_id': todo_id})
    todo['state'] = 'finished'
    c_todo.update({'_id': todo_id}, todo)


# 函数：根据任务的_id，将任务状态更新为“未完成”
def unfinish_todo(todo_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    # 先根据_id查询到任务，再更新任务状态“state”
    todo = c_todo.find_one({'_id': todo_id})
    todo['state'] = 'unfinished'
    c_todo.update({'_id': todo_id}, todo)


# 函数：根据任务的_id，将任务状态更新为“已删除”
def delete_todo(todo_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    # 先根据_id查询到任务，再更新任务状态“state”
    todo = c_todo.find_one({'_id': todo_id})
    todo['state'] = 'deleted'
    c_todo.update({'_id': todo_id}, todo)


# 函数：获取今天的日期(字符串)
def str_today():
    # 获取今天的日期
    today = datetime.date.today()
    # 返回字符串格式的日期
    return str(today)


# 函数：获取昨天的日期(字符串)
def str_yesterday():
    # 昨天的日期 = 今天的日期 - 1天 
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    # 返回字符串格式的日期
    return str(yesterday)