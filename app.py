#!/usr/bin/python3
# coding=utf-8

from flask import Flask, render_template, request, redirect, jsonify, make_response

import auto_bpa
import flask_mysql
import reset_password as rp

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# reply_data = {
#     'sataus': True or False 请求是否按照理想情况运行。理想情况是非定义的。
#     'data': dict 在请求成功的情况下，返回数据或者状态。
#     'error': 仅在 'status' 值为 False 时存在，包含了错误信息。
# }

# API
@app.route('/api/bpa_login', methods = ['POST'])
def bpa_login():
    reply_data = {
        'status': None,
        'data': {},
    }
    print("收到表单数据：%s" % request.form)

    xh = request.form.get('xh')
    passwd = request.form.get('passwd')

    getuser = flask_mysql.getUser(xh)

    reply_data = auto_bpa.login(xh, passwd)

    if getuser['status'] and reply_data['status']:
        if getuser['data']['user'] is None:
            reply_data['register'] = False
        else:
            reply_data['register'] = True
    else:
        reply_data['status'] = False
        reply_data['error'] = "登录失败 查询:%s  登录:%s" % (getuser['status'], reply_data['status'])

    print(reply_data)

    response = make_response(jsonify(reply_data), 200)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "POST"
    return response


@app.route("/api/bpa_adduser", methods = ['POST'])
def bpa_adduser():
    reply_data = {
        'status': None,
        'data': {},
    }
    print("收到表单数据：%s" % request.form)
    try:
        # 转换为字典格式的用户数据
        new_user = request.form.to_dict()
        for i in new_user:
            if new_user[i] == '':
                reply_data['status'] = False
                reply_data['error'] = "提交注册请求失败。error：存在空值。"

                response = make_response(jsonify(reply_data), 200)
                response.headers['Access-Control-Allow-Origin'] = "*"
                response.headers['Access-Control-Allow-Methods'] = "POST"
                return response

        # 提交验证
        reply_data = auto_bpa.new_user_verify(new_user)
    except Exception as e:
        reply_data['status'] = False
        reply_data['error'] = "提交注册请求失败。error：" + str(e)
        print(reply_data)

        response = make_response(jsonify(reply_data), 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = "POST"
        return response
    else:
        print(reply_data)

        response = make_response(jsonify(reply_data), 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = "POST"
        return response


@app.route("/api/bpa_updateuser", methods = ['POST'])
def bpa_updateuser():
    pass


@app.route("/api/bpa_deluser", methods = ['POST'])
def bpa_deluser():
    pass


@app.route("/api/bpa_testbpa", methods = ['POST'])
def bpa_testbpa():
    reply_data = {
        'status': None,
        'data': {}
    }
    print("收到表单数据：%s" % request.form)

    try:
        xh = request.form.get('xh', '')
        if xh == '':
            reply_data['status'] = False
            reply_data['error'] = '学号为空值'
            response = make_response(jsonify(reply_data), 200)
            response.headers['Access-Control-Allow-Origin'] = "*"
            response.headers['Access-Control-Allow-Methods'] = "POST"
            return response

        print("学号：%s 开始尝试测试报平安" % xh)

        get_user = flask_mysql.getUser(xh)

        if get_user['status']:
            user = get_user['data']['user']
            reply_data = auto_bpa.bpa(user, 1)
        else:
            reply_data = get_user
    except Exception as e:
        reply_data = {
            'status': False,
            'data': {},
            'error': '自动化系统错误。位于api_testbpa。error:' + str(type(e)) + str(e)
        }
        response = make_response(jsonify(reply_data), 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = "POST"
        return response
    else:
        response = make_response(jsonify(reply_data), 200)
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers['Access-Control-Allow-Methods'] = "POST"
        return response


# ------------------ 旧的网页 --------------------------
# 其他没用的已删除
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
