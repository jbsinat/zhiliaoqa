from flask import Flask, render_template
# import config

app = Flask(__name__)
# app.config.from_object(config)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test/')
def test():
    return 'test page'


if __name__ == '__main__':
    app.run()
