from flask import Flask, render_template, request
import flask_mysql

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/search', methods = ['POST'])
def seach():
    xh = request.form.get('xh')
    data = flask_mysql.getUser(xh)
    return str(data)

@app.route('/registered', methods = ['POST', 'GET'])
def registerde():
    if request.method == 'GET':
        return render_template('registered.html')
    elif request.method == 'POST':
        req = request.form
        if not flask_mysql.addUser(req):
            return '提交失败'
        else:
            return '提交成功'


if __name__ == '__main__':
    app.run()
