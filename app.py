from flask import Flask, render_template, request, redirect
import flask_mysql
import auto_bpa

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/search', methods = ['POST'])
def search():
    xh = request.form.get('xh')
    reply_data = flask_mysql.getUser(xh)
    if reply_data or reply_data == ():
        if len(reply_data) == 0:
            return render_template('index.html',
                                   cxjg = '<a href = "./registered">用户不存在，点击此链接进行注册。</a>',
                                   )
        else:
            return render_template('index.html',
                                   cxjg = '<a href = "./user?xh=%s">学号%s已找到,点击此链接进行管理。</a>' % (reply_data[0][1], reply_data[0][1]))
    elif not reply_data:
        return '数据库错误导致操作失败!'


@app.route('/registered', methods = ['POST', 'GET'])
def registerdePage():
    if request.method == 'GET':
        return render_template('registered.html')
    elif request.method == 'POST':
        req_data = request.form
        reply_data = flask_mysql.addUser(req_data)
        if reply_data:
            return str(reply_data)
        elif not reply_data:
            return '数据库错误导致操作失败!'


@app.route('/user', methods = ['GET', 'POST'])
def userPage():
    if request.method == 'GET':
        userdata = flask_mysql.getUser(request.args.get('xh'))[0]
        return eval("render_template('user.html',id = '%s',disabled = 'disabled',"
                    "xh = '%s',mm = '%s',xm = '%s',xy = '%s',sjhm = '%s',dz1 = '%s',"
                    "dz2 = '%s',xxdz = '%s',checked1_%s = 'checked',checked2_%s = 'checked',"
                    "email = '%s')"
                    % (userdata[0], userdata[1], userdata[2], userdata[3], userdata[4],
                       userdata[5], userdata[6], userdata[7], userdata[8], userdata[9],
                       userdata[10], userdata[11]))


@app.route('/updateuserdata', methods = ['GET', 'POST'])
def updateUserdata():
    if request.method == 'GET':
        userdata = flask_mysql.getUser(request.args.get('xh'))[0]
        return eval("render_template('updateuserdata.html',id = '%s',"
                    "xh = '%s',mm = '%s',xm = '%s',xy = '%s',sjhm = '%s',dz1 = '%s',"
                    "dz2 = '%s',xxdz = '%s',checked1_%s = 'checked',checked2_%s = 'checked',"
                    "email = '%s')"
                    % (userdata[0], userdata[1], userdata[2], userdata[3], userdata[4],
                       userdata[5], userdata[6], userdata[7], userdata[8], userdata[9],
                       userdata[10], userdata[11]))
    elif request.method == 'POST':
        req_data = request.form.to_dict()
        reply_data = flask_mysql.updateUser(req_data)
        if reply_data:
            return '更新成功!\n返回值->' + str(reply_data)
        elif not reply_data:
            return '数据库错误导致操作失败!'


@app.route('/test_bpa', methods = ['GET', 'POST'])
def test_bpa():
    if request.method == 'GET':
        xh = request.args.get('xh')
        all_user_data = flask_mysql.getUser(xh)
        print(all_user_data)
        try:
            auto = auto_bpa.MainControl(all_user_data)
            del auto
            reply_data = '执行成功'
        except:
            reply_data = '执行失败'
        return reply_data
    elif request.method == 'POST':
        all_user_data = (request.form.to_dict(),)
        try:
            auto = auto_bpa.MainControl(all_user_data)
            reply_data = '执行成功'
            del auto
        except:
            reply_data = '执行失败'
        return reply_data

if __name__ == '__main__':
    app.run()
