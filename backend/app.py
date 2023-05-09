
# -*- coding: UTF-8 -*-
# This project is based on the great work https://github.com/wfloveiu/-----
# Author: Yuyang Zhou
# E-Mail: zhouyuyangmike@foxmail.com

import MySQLdb
from flask import Flask, jsonify, request
from config import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import auth
import json
import random
import datetime
from redis import StrictRedis
from utils import *
import re

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# 跨域
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)

# 添加配置数据库
app.config.from_object(Config)
# 初始化拓展,app到数据库的ORM映射
db = SQLAlchemy(app)

# 检查数据库连接是否成功
with app.app_context():
    with db.engine.connect() as conn:
        query = text("SELECT * FROM user")
        rs = conn.execute(query)
        print(rs.fetchone())

# 用户登录
@app.route("/api/user/login", methods=["POST"])
@cross_origin()
def user_login():
    print('user_login', request.json)
    userid = request.json.get("userid").strip()
    password = request.json.get("password").strip()

    if not re.search(USER_NAME_REGEX, userid):
        return jsonify({"code": 1000, "msg": "用户名不合规范"})
    if not re.search(PASSWORD_REGEX, password):
        return jsonify({"code": 1000, "msg": "密码不合规范"})

    sql = ('select * ' \
           + 'from user ' \
           + 'where userID = "{0}" and password = "{1}"').format(userid, password)
    data = db.session.execute(text(sql)).first()
    print('user_login_data', data)
    if data != None:
        user = {
            'username': data[0],
            'password': data[1],
            'permission': data[2]
        }
        # 生成token
        token = auth.encode_func(user)
        print('user_login_auth', token)
        return jsonify({"code": 200, "msg": "登录成功", "token": token, "permission": data[2]})
    else:
        return jsonify({"code": 1000, "msg": "用户名或密码错误"})


# 用户注册
@app.route("/api/user/register", methods=["POST"])
@cross_origin()
def register():
    rq = request.json
    # 获取验证码和手机号
    username = rq.get("username")
    password = rq.get("password")

    if not re.search(USER_NAME_REGEX, username):
        return jsonify({"status": "1000", "msg": "用户名不合规范"})
    if not re.search(PASSWORD_REGEX, password):
        return jsonify({"status": "1000", "msg": "密码不合规范"})

    sql = ('select * ' \
           + 'from user ' \
           + 'where userID = "{0}"').format(username)
    data = db.session.execute(text(sql)).fetchall()
    if not data:
        sql = ('insert into user(userID, password, superManager) ' \
               + 'value ("{0}", "{1}", False)').format(username, password)
        db.session.execute(text(sql))
        db.session.commit()
        return jsonify({"status": "200", "msg": "注册成功"})
    else:
        return jsonify({"status": "1000", "msg": "该用户已存在"})

@app.route("/api/user/course", methods=["GET", "POST", "ADD", "DELETE"])
@cross_origin()
def user_get_course():
    rq = request.json
    if request.method == "GET":
        permission = rq.get("permission")
        if permission == True:
            sql = 'select * from course'
            data = db.session.execute(sql).fetchall()
            result = []
            for i in range(len(data)):
                info = {
                    'courseID': data[i][0],
                    'courseInfo': data[i][1],
                    'coursePermission': True
                }
                result.append(info)
        
            print('course_info', result)
            return jsonify({"status":"200", "tabledata": result})

        else:
            userID = rq.get('userID')

            sql = ('select course.courseID, course.courseInfo, relation.teacher' \
                   + 'from course as course, userCourseRelationship as relation' \
                   + 'where relation.userID = "{0}" and relation.courseID = course.courseID').format(userID) 
            data = db.session.execute(sql).fetchall()

            result = []
            for i in range(len(data)):
                info = {
                    'courseID': data[i][0],
                    'courseInfo': data[i][1],
                    'coursePermission': data[i][2]
                }
                result.append(info)
        
            print('course_info', result)
            return jsonify({"status":"200", "tabledata": result})

    if request.method == "POST":
        permission = rq.get("permission")
        userID = rq.get("userID")
        courseID = rq.get("courseID")
        if permission != True:
            sql = ('select *' \
                   + 'from userCourseRelationship' \
                   + 'where userID = "{0}" and courseID = course.courseID').format(userID, courseID)

            data = db.session.execute(sql).fetchall()
            if data == None:
                return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseInfo = rq.get("courseInfo")
        sql = ('update course ' \
              + 'set courseInfo = "{0}" ' \
              + 'where courseID = "{1}"').format(courseInfo, courseID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})
    if request.method == "ADD":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseID = rq.get("courseID")
        courseInfo = rq.get("courseInfo")
        sql = ('insert course(courseID, courseInfo) ' \
              + 'value("{0}", "{1}")').format(courseID, courseInfo)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

    if request.method == "DELETE":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseID = rq.get("courseID")
        sql = ('delete from course ' \
              + 'where courseID = "{0}"').format(courseID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

# 超管编辑 用户<-->课程关系
@app.route("/api/user/user_course", methods=["POST", "ADD", "DELETE"])
@cross_origin()
def user_get_user_course():
    rq = request.json
    if request.method == "POST":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseID = rq.get("courseID")
        userID = rq.get("userID")
        teacher = rq.get("teacher")
        sql = ('update userCourseRelationship ' \
              + 'set teacher = {0} ' \
              + 'where courseID = "{1}" and userID = "{2}').format(teacher, courseID, userID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})
    if request.method == "ADD":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseID = rq.get("courseID")
        userID = rq.get("userID")
        teacher = rq.get("teacher")
        sql = ('insert userCourseRelationship(courseID, userID, teacher) ' \
              + 'value("{1}", "{2}", {0})').format(teacher, courseID, userID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

    if request.method == "DELETE":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseID = rq.get("courseID")
        userID = rq.get("userID")
        sql = ('delete from userCourseRelationship ' \
              + 'where courseID = "{0}" and userID = "{1}")').format(courseID, userID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

@app.route("/api/user/lecture", methods=["GET", "POST", "ADD", "DELETE"])
@cross_origin()
def user_get_lecture():
    rq = request.json
    
    if request.method == "GET":
        lecture = rq.get('lecture')
        sql = ('select *' \
               + 'from lecture' \
               + 'where lectureID = "{course}"').format(lecture) 
        data = db.session.execute(sql).fetchall()

        result = []
        for i in range(len(data)):
            info = {
                'lectureID': data[i][0],
                'lectureInfo': data[i][2]
            }
            result.append(info)
        
        print('lecture_info', result)
        return jsonify({"status":"200", "tabledata": result})

    if request.method == "POST":
        # 不允许修改课时所属的课程
        # 修改的话会有很多恶心的问题
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        lectureID = rq.get("lectureID")
        lectureInfo = rq.get("lectureInfo")
        sql = ('update lecture ' \
              + 'set lectureInfo = "{0}" ' \
              + 'where lectureID = "{1}"').format(lectureInfo, lectureID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})
    if request.method == "ADD":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        courseID = rq.get('courseID')
        lectureID = rq.get("lectureID")
        lectureInfo = rq.get("lectureInfo")
        sql = ('insert lecture(lectureID, courseID, lectureInfo) ' \
              + 'value("{0}", "{1}", "{2}")').format(lectureID, courseID, lectureInfo)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

    if request.method == "DELETE":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        lectureID = rq.get("lectureID")
        sql = ('delete from lecture ' \
              + 'where lectureID = "{0}"').format(lectureID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

@app.route("/api/user/homework", methods=["GET", "POST", "ADD", "DELETE"])
@cross_origin()
def user_get_homework():
    rq = request.json
    
    if request.method == "GET":
        homeworkID = rq.get("homeworkID")
        sql = ('select * ' \
                + 'fro homework ' \
                + 'where homeworkID = "{0}"').format(homeworkID)
        data = db.session.execute(sql).fetchall()

        result = []
        for i in range(len(data)):
            info = {
                'homeworkID': data[i][0],
                'homeworkInfo': data[i][2]
            }
            result.append(info)
        
        return jsonify({"status":"200", "tabledata": result})

    if request.method == "POST":

        homeworkID = rq.get("homeworkID")
        homeworkInfo = rq.get("homeworkInfo")
        sql = ('update homework ' \
              + 'set homeworkInfo = "{0}" ' \
              + 'where homeworkID = "{1}"').format(homeworkInfo, homeworkID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})
    if request.method == "ADD":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        homeworkID = rq.get('homeworkID')
        lectureID = rq.get("lectureID")
        homeworkInfo = rq.get("homeworkInfo")
        sql = ('insert lecture(homeworkID, lectureID, homeworkInfo) ' \
              + 'value("{0}", "{1}", "{2}")').format(homeworkID, lectureID, homeworkInfo)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

    if request.method == "DELETE":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})

        lectureID = rq.get("homeworkID")
        sql = ('delete from homework ' \
              + 'where homeworkID = "{0}"').format(homeworkID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

@app.route("/api/user/submission", methods=["GET", "ADD"])
@cross_origin()
def user_get_submission():
    rq = request.json
    
    if request.method == "GET":
        # 查询提交记录
        # (case1)自己不拥有权限所有提交记录
        # (case2)自己拥有权限的课程作业的所有提交记录
        if not permission:
            homeworkID = rq.get('homeworkID')
            userID = rq.get('userID')
            sql = ('select *' \
                   + 'from submission' \
                   + 'where homeworkID = "{0}" and userID = "{1}"').format(homeworkID, userID) 
            data = db.session.execute(sql).fetchall()

            result = []
            for i in range(len(data)):
                info = {
                    'submissionID' : data[i][0],
                    'submissionInfo' : data[i][3],
                    'submissionScore' : data[i][4]
                }
                result.append(info)

            print('homework_info', result)
            return jsonify({"status":"200", "tabledata": result})

        else:
            homeworkID = rq.get('homeworkID')
            userID = rq.get('userID')
            sql = ('select *' \
                   + 'from submission' \
                   + 'where homeworkID = "{0}" ').format(homeworkID) 
            data = db.session.execute(sql).fetchall()

            result = []
            for i in range(len(data)):
                info = {
                    'submissionID': data[i][0],
                    'userID': data[i][1],
                    'submissionInfo': data[i][3],
                    'submissionScore': data[i][4]
                }
                result.append(info)
            
            print('homework_info', result)
            return jsonify({"status":"200", "tabledata": result})

    if request.method == "POST":
        # 不允许修改课时所属的课程
        # 修改的话会有很多恶心的问题
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有作业评分的权限"})

        submissionID = rq.get("submissionID")
        submissionScore = rq.get("submissionScore")
        if submissionScore < 0 or submissionScore > 100:
            return jsonify({"status": "1000", "msg": "评分需要落在 [0,100] 范围内"})
        sql = ('update submission ' \
              + 'set submissionScore = "{0}" ' \
              + 'where submissionID = "{1}"').format(submissionScore, submissionID)
        db.session.execute(sql)
        db.session.commit()

        return jsonify({"status":"200", "msg": "修改成功"})

    if request.method == "ADD":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有提交作业的权限"})

        submissionID = rq.get('submissionID')
        userID = rq.get('userID')
        lectureID = rq.get("lectureID")
        submissionInfo = rq.get("submissionInfo")
        sql = ('insert subission(submissionID, userID, lectureID, submissionInfo, submissionScore) ' \
              + 'value("{0}", "{1}", "{2}", "{3}", Null)').format(submissionID, userID, lectureID, submissionInfo)
        db.session.execute(sql)
        db.session.commit()
        return jsonify({"status":"200", "msg": "修改成功"})


@app.route("/api/user/pwd_chg", methods=["POST"])
@cross_origin()
def user_pwd_chg():
    rq = request.json
    if request.method=='POST':
        userID = rq.get('userID')
        password = rq.get('password')
        new_password = rq.get('new_password')
# FPE*CS93SSVSCL
        sql = ('select * ' \
              + 'from user ' \
              + ' where userID = "{0}" and password = "{1}"').format(userID, password)
        data = db.session.execute(sql).fetchall()
        if not data:
            return jsonify(status=1000,msg="原始密码错误")
        else:
            sql = ('update user set password = "{0}"' \
                  + 'where userID = "{1}"').format(userID, new_password)
            db.session.execute(sql)
            db.session.commit()
            return jsonify(status=200,msg="修改成功")