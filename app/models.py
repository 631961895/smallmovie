#-*- encoding:utf-8 -*-
# Author:lijunyi
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123@127.0.0.1:3306/movie"
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    name = db.Column(db.String(100),unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100),unique=True)  # 邮箱
    phone = db.Column(db.String(11),unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255),unique=True)  # 头像
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255),unique=True)  # 唯一标识
    userlogs = db.relationship('Userlog',backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment',backref='user')  # 会员评论外键关系关联
    moviecols = db.relationship('Moviecol',backref='user')  # 会员收藏外键关系关联

    def __str__(self):
        return f"<User {self.name}>"


# 会员登录日志
class Userlog(db.Model):
    __tablenam__ = "userlog"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  # 所属会员，外键关联user表id
    ip = db.Column(db.String(100)) # 登录ip
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 登录时间

    def __str__(self):
        return f"<Userlog {self.id}>"


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    name = db.Column(db.String(100),unique=True)  # 标题
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 添加时间
    movies = db.relationship("Movie",backref="tag")  # 电影外键关系关联

    def __str__(self):
        return f"Tag {self.name}"


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    title = db.Column(db.String(255),unique=True)  # 标题
    url = db.Column(db.String(255),unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255),unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer,db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 添加时间
    comments = db.relationship("Comment",backref="movie")  # 评论电影外键关系关联
    moviecols = db.relationship('Moviecol',backref='movie')  # 电影收藏外键关系关联

    def __str__(self):
        return f"<Movie {self.title}>"


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    title = db.Column(db.String(255),unique=True)  # 标题
    logo = db.Column(db.String(255),unique=True)  # 封面
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 添加时间

    def __str__(self):
        return f"<Preview {self.title}>"


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 添加时间

    def __str__(self):
        return f"Comment {self.id}"


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    movie_id = db.Column(db.Integer,db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 添加时间

    def __str__(self):
        return f"Moviecol {self.id}"


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __str__(self):
        return f"Auth {self.name}"


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 拥有权限
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin',backref='role')  # 管理员角色外键关系关联

    def __str__(self):
        return f"Role {self.name}"


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员
    role_id = db.Column(db.Integer,db.ForeignKey("role.id")) # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship('Adminlog',backref='admin')  # 管理员登录日志外键关系关联
    oplogs = db.relationship('Oplog',backref='admin')  # 管理员操作日志外键关系关联

    def __str__(self):
        return f"Admin {self.name}"


# 管理员登录日志
class Adminlog(db.Model):
    __tablenam__ = "adminlog"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))  # 所属会员，外键关联user表id
    ip = db.Column(db.String(100)) # 登录ip
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 登录时间

    def __str__(self):
        return f"<Adminlog {self.id}>"


# 管理员操作日志
class Oplog(db.Model):
    __tablenam__ = "oplog"
    id = db.Column(db.Integer,primary_key=True)  # 编号
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))  # 所属会员，外键关联user表id
    ip = db.Column(db.String(100)) # 登录ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime,index=True,default=datetime.now)  # 登录时间

    def __str__(self):
        return f"<Oplog {self.id}>"


if __name__ == "__main__":
    # db.create_all()
    role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()

    from werkzeug.security import generate_password_hash
    admin = Admin(
        name="imoocmovie",
        pwd=generate_password_hash("imoocmovie"),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()

