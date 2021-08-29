from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/search', methods = ['POST'])
def seach():
    if request.form['xh'] == '1701070235':
        return 'test success'


if __name__ == '__main__':
    app.run()
