#!/usr/bin/python3
# coding=utf-8

from flask import Flask, render_template, request, redirect
import flask_mysql
import auto_bpa
import reset_password as rp

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
        req_data = request.form.to_dict()
        if len(flask_mysql.getUser(req_data['xh'])) != 0:
            return render_template('registered.html',
                                   tips = '<h3 style="color: red">错误：数据库内已有此学号数据</h3>'
                                          '<a href="/">您可以直接点击此链接回到主页</a>')
        reply_data = flask_mysql.addUser(req_data)
        if reply_data:
            user = ['', req_data['xh'], req_data['mm'], req_data['xm'], req_data['xy'], req_data['sjhm'], req_data['dz1'], req_data['dz2'], req_data['xxdz'], req_data['tw1'], req_data['tw2'], req_data['email']]
            auto_bpa.new_user_verify(user)
            return redirect('/user?xh=%s&command=show_newuser' % req_data['xh'])
        elif not reply_data:
            return '数据库错误导致操作失败!'


@app.route('/user', methods = ['GET', 'POST'])
def userPage():
    if request.method == 'GET':
        userdata = flask_mysql.getUser(request.args.get('xh'))[0]
        if userdata[12] == 1:
            zt = '未验证，您可以点击下方验证数据进行验证'
        elif userdata[12] == 2:
            zt = '验证失败，请更新数据后点击下方验证数据进行验证'
        elif userdata[12] == 0:
            zt = '验证通过，数据有效'
        else:
            zt = userdata[12]
        if request.args.get('command', '') == 'show_newuser':
            tips = '<h3 style="color: green">注册成功！以下是您的数据</h3>' \
                   '<h3 style="color: green">另外我们向您的邮箱发送了验证邮件请注意查收。</h3>'
        else:
            tips = ''
        return eval("render_template('user.html',id = '%s',disabled = 'disabled',"
                    "xh = '%s',mm = '%s',xm = '%s',xy = '%s',sjhm = '%s',dz1 = '%s',"
                    "dz2 = '%s',xxdz = '%s',checked1_%s = 'checked',checked2_%s = 'checked',"
                    "email = '%s',tips = '%s',zt = '%s')"
                    % (userdata[0], userdata[1], userdata[2], userdata[3], userdata[4],
                       userdata[5], userdata[6], userdata[7], userdata[8], userdata[9],
                       userdata[10], userdata[11], tips, zt))


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
            return '<p>更新成功!</p>' \
                   '<a href="/">回到主页</a>'
        elif not reply_data:
            return '数据库错误导致操作失败!'


@app.route('/test_bpa', methods = ['POST'])
def test_bpa():
    if request.method == 'POST':
        xh = request.form.get('xh', '')
        user = list(flask_mysql.getUser(xh)[0])
        print(user)
        try:
            auto_bpa.new_user_verify(user)
            reply_data = '执行成功'
        except:
            reply_data = '执行失败'
        return reply_data


@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('rest_password.html',
                               ui = '''
                               <p>输入您想修改密码的学号</p>
                                <form action = "./reset_password?command=sendmail" method = "post">
                                    <p><label>
                                        <input type = "text" name = "xh" maxlength = 10 />
                                    </label><input type = "submit" value = "查询" /></p>
                                </form>''')
    if request.method == 'POST' and request.args.get('command') == 'sendmail':
        xh = request.form.get('xh', '')
        tips = rp.send_verify_code(xh)
        return render_template('rest_password.html',
                               ui = '''
                                       <p>输入验证码以及新密码</p>
                                        <form action = "./reset_password?command=changepassword" method = "post">
                                            <input type = "text" name = "xh" value = '%s' hidden/>
                                            <p><label>验证码：
                                                <input type = "text" name = "code"/>
                                            </label></p>
                                            <p><label>
                                            新密码：
                                                <input type = "text" name = "new_password"/>
                                            </label></p>
                                            <p><input type = "submit" value = "提交修改" /></p>
                                        </form>''' % xh,
                               cxjg = '<p>我们已经向邮箱：%s 发送了一串验证码，请注意查收。</p>' % tips['tips'].get('result', '请求失败！'))
    elif request.method == 'POST' and request.args.get('command') == 'changepassword':
        xh = request.form.get('xh', '')
        code = request.form.get('code', '')
        new_password = request.form.get('new_password', '')
        q = rp.reset_password(xh, code, new_password)
        print(q)
        if q.get('success'):
            return render_template('rest_password.html',
                                   ui = '''
                                       <p>恭喜，没报错，应该可能成功了</p>
                                       <p>如您已注册，那么新密码已同步提交到自动化服务器。您可以重新进入主页重新查询。</p>
                                       <a href='/'>点击此链接回到主页</a>
                                        ''',
                                   cxjg = '')
        elif not q.get('success'):
            return render_template('rest_password.html',
                                   ui = '''
                                       <p>修改失败！请尝试重新修改</p>
                                        <form action = "./reset_password?command=changepassword" method = "post">
                                            <input type = "text" name = "xh" value = '%s' hidden/>
                                            <p><label>验证码：
                                                <input type = "text" name = "code" value = '%s'/>
                                            </label></p>
                                            <p><label>
                                            新密码：
                                                <input type = "text" name = "new_password"/>
                                            </label></p>
                                            <p><input type = "submit" value = "提交修改" /></p>
                                        </form>''' % (xh, code),
                                   cxjg = '<p style="color: red">修改失败。错误消息：%s </p>' % q.get('message', '请求失败！'))


if __name__ == '__main__':
    app.run()
