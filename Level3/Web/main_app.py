from flask import Flask, render_template,request,redirect,session
import time
import ybc_trans as trans

from trans_app import trans_app
from user_app import user_app
from todo_app import todo_app
from album_app import album_app


app = Flask(__name__)
app.secret_key = 'anbio3h4i34og'

app.register_blueprint(trans_app)
app.register_blueprint(user_app)
app.register_blueprint(todo_app)
app.register_blueprint(album_app)

@app.route('/')
def welcome():
    return render_template('welcome.html',t_name=('Pikaber'))

@app.route('/home')
def home():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('main.html',t_time=today_time)

@app.route('/work-tool')
def worktool():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('worktool.html',t_time=today_time)

@app.route('/web-tool')
def webtool():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('webtool.html',t_time=today_time)

@app.route('/game')
def game():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('game.html',t_time=today_time)

@app.route('/other')
def other():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('other.html',t_time=today_time)

@app.route('/schedule')
def schdule():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('schedule.html',t_time=today_time)

@app.route('/none')
def none():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/minecraft')
def mc():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/atc')
def atc():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/fsx')
def fsx():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/ksp')
def ksp():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/xplane')
def xplane():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/i-f')
def infiniteflight():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/csair')
def csa():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/creepercraft')
def creepercraft():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/salmonaviation')
def salmonaviation():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/email')
def email():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('1.html',t_time=today_time)

@app.route('/sgin-up')
def sginup():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('sginup_page.html',t_time=today_time)

@app.route('/login')
def login():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('login_page.html',t_time=today_time)

@app.route('/help')
def help():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('help.html',t_time=today_time)

@app.route('/welcome')
def welcome2():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('2.html',t_time=today_time)

@app.route('/sgin_up_ok')
def sginupok():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('sginupok.html',t_time=today_time)

@app.route('/loginok')
def loginok():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('loginok.html',t_time=today_time)

@app.route('/get')
def form_get():
    name = request.args['nickname']
    return 'hello!成功提交数据，数据提交方式为get，数据为“ ' + name + ' ”'

@app.route('/post', methods=['POST'])
def form_post():
    name = request.form['nickname']
    return 'hello!成功提交数据，数据提交方式为post，数据为“ ' + name + ' ”'

@app.route('/test_page_1')
def person_info():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('info.html', t_time=today_time)

@app.route('/test_page_2')
def test_page_2():
    today_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render_template('not_test_now.html',t_time=today_time)



@app.route('/trans')
def index():
    return render_template('trans3.html')

@app.route('/do_trans')
def translation():
    txt = request.args['txt']
    op = request.args['op']
    if op == '英译汉' :
        result = trans.en2zh(txt)
    elif op == '汉译英' :
        result = trans.zh2en(txt)
    return render_template('trans3.html', t_txt=txt, t_result=result, t_op=op)


@app.route('/welcome')
def welcome():
    return render_template('main/welcome.html', t_my_name='壮猿')

@app.route('/main')
def main():
    username = session.get('username')
    if username != None:
        is_login = True
    else:
        is_login = False
        username = '游客'
    return render_template('main/main.html', t_username=username, t_is_login=is_login)

if __name__ == '__main__':
    app.run(port=5001)