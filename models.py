# 用于定义各种模型对象

from exts import db
from datetime import datetime
# flask框架提供的一个密码加密函数
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        # 将密码明文加密后再存储到数据库中
        self.password = generate_password_hash(password)

    # 定义一个检查用户密码的函数
    def check_password(self, raw_password):
        # check_password_hash()函数返回一个 bool 值
        result = check_password_hash(self.password, raw_password)
        return result


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('articles'))

# author = db.relationship('User', backref=db.backref('articles'))解释：
# 给'Article'这个模型添加一个'author'属性，可以访问这篇文章的作者的数据，像访问普通模型一样
# 'backref'是定义反向引用，可以通过'User.articles'访问这个模型所写的所有文章


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 这里只能用now而不能用now(),因为不是引用函数
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))
