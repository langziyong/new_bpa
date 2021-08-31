from flask import Flask, render_template, request
import flask_mysql

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
                                   cxjg = '<a>学号%s已找到，共%s条记录！点击此链接进行管理。</a>' % (reply_data[0][1], len(reply_data)))
    elif not reply_data:
        return '数据库错误导致动作失败!'


@app.route('/registered', methods = ['POST', 'GET'])
def registerde():
    if request.method == 'GET':
        return render_template('registered.html')
    elif request.method == 'POST':
        req_data = request.form
        reply_data = flask_mysql.addUser(req_data)
        if reply_data:
            return str(reply_data)
        elif not reply_data:
            return '数据库错误导致动作失败!'


if __name__ == '__main__':
    app.run()
