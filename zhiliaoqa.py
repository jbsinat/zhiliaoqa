from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from models import User, Question, Answer
# 引入db，为了下面的查询语句能生效
from exts import db
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
# 引入db后还要再配置db，否则无法使用查询等操作数据库的语句
db.init_app(app)


@app.route('/')
def index():
    context = {
        # order_by('-create_time')中的 '-' 表示从近到远
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号或密码错误，请确认后重新登录'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 用户手机号验证，如果被注册了，就不能再注册了
        # .first()用于获取查询到的list中的第一条数据，如果没有，则会返回null
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号已被注册'
        else:
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()  # 数据库相关操作之后一定要手动提交
                # 如果验证成功，跳转到登录页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # 1：session.pop('user_id')
    # 2：del session['user_id']
    session.clear()  # 将session中的数据全删除
    return redirect(url_for('login'))


@app.route('/question/', methods=['GET', 'POST'])
def question():
    user_id = session.get('user_id')
    if user_id:
        if request.method == 'GET':
            return render_template('question.html')
        else:
            title = request.form.get('title')
            content = request.form.get('content')
            create_time = datetime.now()
            author_id = session.get('user_id')
            q = Question(title=title, content=content, create_time=create_time, author_id=author_id)
            db.session.add(q)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return u'请先登录'


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer/', methods=['POST'])
def add_answer():
    user_id = session.get('user_id')
    if user_id:
        answer_content = request.form.get('answer_content')
        question_id = request.form.get('question_id')
        answer = Answer(content=answer_content)
        answer.author = g.user
        q = Question.query.filter(Question.id == question_id).first()
        answer.question = q
        # answer.question_id = question_id
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail', question_id=question_id))
    else:
        return redirect(url_for('login'))


@app.route('/search/')
def search():
    q = request.args.get('q')
    # 或
    condition = or_(or_(Question.title.contains(q), Question.content.contains(q)))
    questions = Question.query.filter(condition).order_by('-create_time')
    return render_template('index.html', questions=questions)


# 钩子函数
# 将user放到g（相当于全局变量）中
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


# 上下文处理器，返回一个字典，字典中的'key'会被模板中当成变量来渲染，在所有页面都是可用的
@app.context_processor
def my_context_processor():
    # hasattr用来判断 g 中是否有user这个属性
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


# 钩子函数
# 在请求之前执行，是在视图函数执行之前执行的；
# 只是一个装饰器，可以把需要设置为钩子函数的代码放到视图函数渲染之前执行
# @app.before_request
# def login_required():
#     user_id = session.get('user_id')
#     if user_id:
#         pass
#     else:
#         return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
