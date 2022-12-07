# 从flask模块中，导入蓝图Blueprint
from flask import Blueprint, render_template, request, redirect, session
import uuid
import pymongo

# 【提示 4】创建蓝图对象album_app，名称为"album_app"
album_app = Blueprint('album_app',__name__)


# 使用蓝图对象album_app，创建与“相册功能”有关的路由

# 路由：返回相册列表页面
@album_app.route('/album_list')
def album_list():
    all_album_list = find_all_album()

    album_list = []

    for info in all_album_list:
        albumname = info['albumname']
        imgs = info['imgs']
        num = len(imgs)

        album = {'albumname': albumname, 'num': num, 'img_path': imgs[0]}

        album_list.append(album)

    username = session.get('username')
    if username == None:
        username = "游客"

    return render_template('album/album_list.html', t_album_list=album_list, t_username=username)

# 路由：返回图片列表页面
@album_app.route('/image_list')
def image_list():
    albumname = request.args['albumname']
    print(albumname)

    album = find_album(albumname)

    imgs_list = album['imgs']
    print(imgs_list)

    username = session.get('username')
    if username == None:
        username = "游客"

    return render_template('album/image_list.html',
                           t_albumname=albumname,
                           t_imgs_list=imgs_list,
                           t_username=username)

# 路由：返回创建相册页面
@album_app.route('/create')
def create():
    username = session.get('username')
    if username == None:
        username = "游客"
    return render_template('album/create_album.html', t_username=username)


# 路由：处理创建相册页面的表单
@album_app.route('/create_check', methods=['POST'])
def create_check():
    # 获取用户上传的图片文件对象
    img = request.files['img']
    # 获取图片的文件名
    filename = img.filename
    # 使用uuid防止文件名重名
    filename = str(uuid.uuid1()) + filename
    # 设置图片的存储路径：这里使用相对路径，切记不可使用/开头
    img_path = 'static/album/upload/' + filename
    # 将图片保存到指定的路径
    img.save(img_path)

    albumname = request.form['albumname']

    album = find_album(albumname)

    if album == None:

        imgs = [img_path]

        new_album = {'albumname': albumname, 'imgs': imgs}

        insert_album(new_album)

        return redirect('/album_list')

    else:
        username = session.get('username')
        if username == None:
            username = "游客"

        return render_template('album/create_album.html',
                               t_albumname=albumname,
                               t_error='该相册已存在',
                               t_username=username)


@album_app.route('/upload')
def upload():
    username = session.get('username')
    if username == None:
        username = "游客"

    album_list = find_all_album()
    return render_template('album/upload.html', t_album_list=album_list, t_username=username)


@album_app.route('/upload_check', methods=['POST'])
def upload_check():
    # 获取用户上传的图片文件对象
    img = request.files['img']
    # 获取图片的文件名
    filename = img.filename
    # 使用uuid防止文件名重名
    filename = str(uuid.uuid1()) + filename
    # 设置图片的存储路径：这里使用相对路径，切记不可使用/开头
    img_path = 'static/album/upload/' + filename
    # 将图片保存到指定的路径
    img.save(img_path)

    albumname = request.form['albumname']

    update_album(albumname, img_path)

    return redirect('/album_list')


'''
    --------自定义函数--------

    insert_album()       将“某个相册的数据”存储到数据库中
    find_album()         从数据库中“根据相册名”获取该相册的数据
    find_all_album()     从数据库中获取所有相册的数据
    update_album()       更新数据库中某个相册的数据

'''


# 将“某个新相册的数据”存储到数据库中
def insert_album(album):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    c_album.insert_one(album)


# 从数据库中“根据相册名”获取该相册的数据
def find_album(albumname):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    condition = {'albumname': albumname}
    album = c_album.find_one(condition)
    return album


# 从数据库中获取所有相册的数据
def find_all_album():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    res = c_album.find()
    album_list = []
    for album in res:
        album_list.append(album)
    return album_list


# 根据相册名 从数据库中 更新某个相册的数据
def update_album(albumname, img_path):
    # 链接数据库集合
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    condition = {'albumname': albumname}
    # 根据相册名找到该相册字典
    album = c_album.find_one(condition)
    # 找到字典中imgs键对应的图片列表
    imgs_list = album['imgs']
    # 在图片列表中添加新图片的路径
    imgs_list.append(img_path)
    # 更新
    c_album.update(condition, album)

