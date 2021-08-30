from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/search', methods = ['POST'])
def seach():
    pass


@app.route('/registered', methods = ['POST', 'GET'])
def registerde():
    if request.method == 'GET':
        return render_template('registered.html')


if __name__ == '__main__':
    app.run()
