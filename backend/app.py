
# -*- coding: UTF-8 -*-
# This project is based on the great work https://github.com/wfloveiu/-----
# Author: Yuyang Zhou and Rundong Luo
# Email: {2000013061, rundong_luo}@stu.pku.edu.cn

from flask_cors import cross_origin
from flask_cors import CORS
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
redis_store = StrictRedis(host=Config.REDIS_HOST,
                          port=Config.REDIS_PORT, decode_responses=True)

# 跨域

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

    # debug: print userid and password
    print('user_login_userid', userid, 'user_login_password', password)

    if not re.search(USER_NAME_REGEX, userid):
        return jsonify({"code": 1000, "msg": "用户名不合规范"})
    if not re.search(PASSWORD_REGEX, password):
        return jsonify({"code": 1000, "msg": "密码不合规范"})

    sql = ('select * '
           + 'from user '
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

    sql = ('select * '
           + 'from user '
           + 'where userID = "{0}"').format(username)
    data = db.session.execute(text(sql)).fetchall()
    if not data:
        sql = ('insert into user(userID, password, superManager) '
               + 'value ("{0}", "{1}", False)').format(username, password)
        db.session.execute(text(sql))
        db.session.commit()
        return jsonify({"status": "200", "msg": "注册成功"})
    else:
        return jsonify({"status": "1000", "msg": "该用户已存在"})


@app.route("/api/user/course", methods=["GET", "POST", "ADD", "DELETE"])
@cross_origin()
def user_get_course():
    print("Request Method:", request.method)  # 添加调试信息
    print('user_get_course', request.args.get("permission"))
    if request.method == "GET":
        rq = request.args
        permission = rq.get("permission")
        if permission == 'admin':
            sql = 'select * from course'
            data = db.session.execute(text(sql)).fetchall()
            result = []
            for i in range(len(data)):
                info = {
                    'courseID': data[i][0],
                    'courseName': data[i][1],
                    'courseInfo': data[i][2],
                    'coursePermission': True
                }
                result.append(info)

            print('course_info', result)
            return jsonify({"status": "200", "tabledata": result})

        else:
            print('user_get_course', request.args.get("userID"))
            userID = rq.get('userID')

            # 获取学生课程
            student_sql = ('select course.courseID, course.courseName, course.courseInfo, relation.teacher '
                           'from course as course, userCourseRelationship as relation '
                           'where relation.userID = "{0}" and relation.courseID = course.courseID and relation.teacher = 0').format(userID)
            student_data = db.session.execute(text(student_sql)).fetchall()

            # 获取教师课程
            teacher_sql = ('select course.courseID, course.courseName, course.courseInfo, relation.teacher '
                           'from course as course, userCourseRelationship as relation '
                           'where relation.userID = "{0}" and relation.courseID = course.courseID and relation.teacher = 1').format(userID)
            teacher_data = db.session.execute(text(teacher_sql)).fetchall()

            student_result = []
            teacher_result = []

            for i in range(len(student_data)):
                info = {
                    'courseID': student_data[i][0],
                    'courseName': student_data[i][1],
                    'courseInfo': student_data[i][2],
                    'coursePermission': student_data[i][3]
                }
                student_result.append(info)

            for i in range(len(teacher_data)):
                info = {
                    'courseID': teacher_data[i][0],
                    'courseName': teacher_data[i][1],
                    'courseInfo': teacher_data[i][2],
                    'coursePermission': teacher_data[i][3]
                }
                teacher_result.append(info)

            return jsonify({"status": "200", "student_courses": student_result, "teacher_courses": teacher_result})

    if request.method == "POST":

        rq = request.get_json()
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})
        
        if rq.get("method") == "ADD":

            courseID = rq.get("courseID")
            courseName = rq.get("courseName")
            courseInfo = rq.get("courseInfo")
            # check if cannot insert
            sql = ('select * from course where courseID = {0}').format(courseID)
            data = db.session.execute(text(sql)).fetchall()
            if data:
                return jsonify({"status": "1000", "msg": "课程ID已存在"})
            
            sql = ('insert course(courseID, courseName, courseInfo) '
                + 'value({0}, "{1}", "{2}")').format(courseID, courseName, courseInfo)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        elif rq.get("method") == "DELETE":
            courseID = rq.get("courseID")
            sql = ('delete from course '
                + 'where courseID = {0}').format(courseID)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        else:
            return jsonify({"status": "1000", "msg": "method参数错误"})


# 超管编辑 用户<-->课程关系
@app.route("/api/user/user_course", methods=["GET", "POST"])
@cross_origin()
def user_get_user_course():
    print("user get user course")
    
    print("Request Method:", request.method)  # 添加调试信息
    if request.method == "GET":
        course_id = request.args.get("courseID")

        # 获取教师信息
        teacher_sql = ('select userID from userCourseRelationship '
                       'where courseID = {0} and teacher = 1').format(course_id)
        teacher_data = db.session.execute(text(teacher_sql)).fetchall()

        # 获取学生信息
        student_sql = ('select userID from userCourseRelationship '
                       'where courseID = {0} and teacher = 0').format(course_id)
        student_data = db.session.execute(text(student_sql)).fetchall()

        teacher_list = [row[0] for row in teacher_data]
        student_list = [row[0] for row in student_data]

        # 获取courseName和courseInfo
        course_sql = ('select courseName, courseInfo from course '
                        'where courseID = {0}').format(course_id)
        course_data = db.session.execute(text(course_sql)).fetchall()
        course_name = course_data[0][0]
        course_info = course_data[0][1]

        return jsonify({"status": "200", "courseName": course_name, "courseInfo": course_info, "teachers": teacher_list, "students": student_list})

    if request.method == "POST":
        rq = request.json
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})
        
        method = rq.get("method")
        if method == "ADD":
            courseID = rq.get("courseID")
            userID = rq.get("userID")
            teacher = rq.get("teacher")
            # check if cannot insert
            sql = ('select * from userCourseRelationship where courseID = {0} and userID = "{1}"').format(courseID, userID)
            data = db.session.execute(text(sql)).fetchall()
            if data:
                return jsonify({"status": "1000", "msg": "用户已存在"})
            # check if not a user
            sql = ('select * from user where userID = "{0}"').format(userID)
            data = db.session.execute(text(sql)).fetchall()
            if not data:
                return jsonify({"status": "1000", "msg": "用户不存在"})
            sql = ('insert userCourseRelationship(courseID, userID, teacher) '
                 'value({1}, "{2}", {0})').format(teacher, courseID, userID)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        elif method == "DELETE":
            courseID = rq.get("courseID")
            userID = rq.get("userID")
            sql = ('delete from userCourseRelationship '
                 'where courseID = {0} and userID = "{1}"').format(courseID, userID)
            print(sql)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        else:
            return jsonify({"status": "1000", "msg": "method参数错误"})


@app.route("/api/user/lecture", methods=["GET", "POST"])
@cross_origin()
def user_get_lecture():
    print("Lecture, Request Method:", request.method)  # 添加调试信息
    if request.method == "GET":
        courseID = request.args.get("courseID")
        sql = ('select * '
               'from lecture '
               'where courseID = {0}').format(courseID)
        data = db.session.execute(text(sql)).fetchall()

        result = []
        for i in range(len(data)):
            info = {
                'lectureID': data[i][0],
                'lectureInfo': data[i][2]
            }
            result.append(info)

        print('lecture_info', result)
        return jsonify({"status": "200", "tabledata": result})

    if request.method == "POST":
        rq = request.json
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有修改课程的权限"})
        
        method = rq.get("method")
        if method == 'ADD':
            lectureInfo = rq.get("lectureInfo")
            lectureID = rq.get("lectureID")
            courseID = rq.get("courseID")
            print(lectureInfo, lectureID, courseID)
            # check if cannot insert
            sql = ('select * from lecture where lectureID = {0} and courseID = {1}').format(lectureID, courseID)
            data = db.session.execute(text(sql)).fetchall()
            if data:
                return jsonify({"status": "1000", "msg": "课时ID已存在"})
            sql = ('insert lecture(lectureID, courseID, lectureInfo) '
                + 'value({0}, {1}, "{2}")').format(lectureID, courseID, lectureInfo)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        elif method == 'UPDATE':
            courseID = rq.get("courseID")
            lectureID = rq.get("lectureID")
            lectureInfo = rq.get("lectureInfo")
            # check if cannot insert, (courseID and lectureID) is primary key
            sql = ('select * from lecture where lectureID = {0} and courseID = {1}').format(lectureID, courseID)
            data = db.session.execute(text(sql)).fetchall()
            if not data:
                return jsonify({"status": "1000", "msg": "课时不存在"})
            
            sql = ('update lecture '
                + 'set lectureInfo = "{0}" '
                + 'where lectureID = {1} and courseID = {2}').format(lectureInfo, lectureID, courseID)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})

        elif method == 'DELETE':
            courseID = rq.get("courseID")
            lectureID = rq.get("lectureID")
            sql = ('delete from lecture '
                + 'where lectureID = {0} and courseID = {1}').format(lectureID, courseID)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})


@app.route("/api/user/assignment", methods=["GET", "POST"])
@cross_origin()
def user_get_assignment():
    if request.method == "GET":
        courseID = request.args.get("courseID")
        sql = ('select * '
               'from assignment '
               'where courseID = {0}').format(courseID)
        data = db.session.execute(text(sql)).fetchall()

        result = []
        for i in range(len(data)):
            info = {
                'assignmentID': data[i][0],
                'assignmentInfo': data[i][2]
            }
            result.append(info)

        return jsonify({"status": "200", "tabledata": result})

    if request.method == "POST":
        rq = request.json
        method = rq.get("method")
        if method == 'ADD':
            assignmentID = rq.get("assignmentID")
            courseID = rq.get("courseID")
            assignmentInfo = rq.get("assignmentInfo")
            # check if cannot insert, (courseID and assignmentID) is primary key
            sql = ('select * from assignment where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
            data = db.session.execute(text(sql)).fetchall()
            if data:
                return jsonify({"status": "1000", "msg": "作业ID已存在"})
            sql = ('insert assignment(assignmentID, courseID, assignmentInfo) '
                + 'value({0}, {1}, "{2}")').format(assignmentID, courseID, assignmentInfo)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        elif method == 'UPDATE':
            assignmentID = rq.get("assignmentID")
            courseID = rq.get("courseID")
            assignmentInfo = rq.get("assignmentInfo")
            # check if cannot insert, assignmentID is primary key
            sql = ('select * from assignment where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
            data = db.session.execute(text(sql)).fetchall()
            if not data:
                return jsonify({"status": "1000", "msg": "作业不存在"})
            sql = ('update assignment '
                + 'set assignmentInfo = "{0}" '
                + 'where assignmentID = {1} and courseID = {2}').format(assignmentInfo, assignmentID, courseID)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})
        
        elif method == 'DELETE':
            assignmentID = rq.get("assignmentID")
            courseID = rq.get("courseID")
            sql = ('delete from assignment '
                + 'where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
            db.session.execute(text(sql))
            db.session.commit()

            return jsonify({"status": "200", "msg": "修改成功"})

@app.route("/api/user/submission", methods=["POST"])
@cross_origin()
def user_get_submission():
    rq = request.json
    method = rq.get("method")

    if method == "GET":
        # 查询提交记录
        # (case1)自己不拥有权限所有提交记录
        # (case2)自己拥有权限的课程作业的所有提交记录
        permission = rq.get('permission')
        print(permission)
        if not permission:
            assignmentID = rq.get('assignmentID')
            userID = rq.get('userID')
            courseID = rq.get('courseID')
            sql = ('select * '
                   'from assignment '
                   'where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
            data = db.session.execute(text(sql)).fetchall()
            if not data:
                return jsonify({"status": "1000", "msg": "作业与课程不匹配"})
            
            sql = ('select * '
                   'from submission '
                   'where assignmentID = {0} and userID = "{1}" and courseID = {2}').format(assignmentID, userID, courseID)
            data = db.session.execute(text(sql)).fetchall()

            result = []
            for i in range(len(data)):
                info = {
                    'submissionID': data[i][0],
                    'submissionInfo': data[i][4],
                    'submissionScore': data[i][5]
                }
                result.append(info)

            print('assignment_info', result)
            return jsonify({"status": "200", "tabledata": result})

        else:
            assignmentID = rq.get('assignmentID')
            courseID = rq.get('courseID')
            # primary key: (assignmentID, courseID)
            sql = ('select * '
                   'from assignment '
                   'where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
            data = db.session.execute(text(sql)).fetchall()
            if not data:
                return jsonify({"status": "1000", "msg": "作业与课程不匹配"})
            sql = ('select * '
                    'from submission '
                    'where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
            data = db.session.execute(text(sql)).fetchall()

            result = []
            for i in range(len(data)):
                info = {
                    'submissionID': data[i][0],
                    'userID': data[i][1],
                    'submissionInfo': data[i][4],
                    'submissionScore': data[i][5]
                }
                result.append(info)

            print('assignment_info', result)
            return jsonify({"status": "200", "tabledata": result})

    elif method == "UPDATE":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有作业评分的权限"})

        submissionID = rq.get("submissionID")
        submissionScore = rq.get("score")
        submissionScore = int(submissionScore)
        if submissionScore < 0 or submissionScore > 100:
            return jsonify({"status": "1000", "msg": "评分需要落在 [0,100] 范围内"})
        sql = ('update submission '
               + 'set submissionScore = "{0}" '
               + 'where submissionID = {1}').format(submissionScore, submissionID)
        db.session.execute(text(sql))
        db.session.commit()

        return jsonify({"status": "200", "msg": "修改成功"})

    elif method == "SUBMIT":
        permission = rq.get("permission")
        if permission != True:
            return jsonify({"status": "1000", "msg": "没有提交作业的权限"})

        userID = rq.get('userID')
        courseID = rq.get('courseID')
        assignmentID = rq.get('assignmentID')
        submissionInfo = rq.get("submissionInfo")
        sql = ('select * '
               'from assignment '
               'where assignmentID = {0} and courseID = {1}').format(assignmentID, courseID)
        data = db.session.execute(text(sql)).fetchall()
        if not data:
            return jsonify({"status": "1000", "msg": "作业与课程不匹配"})
        
        sql = ('select * '
               'from userCourseRelationship '
               'where userID = {0} and courseID = {1}').format(userID, courseID)
        data = db.session.execute(text(sql)).fetchall()
        if not data:
            return jsonify({"status": "1000", "msg": "用户与课程不匹配"})

        sql = ('insert submission (userID, assignmentID, courseID, submissionInfo) '
               'value("{0}", {1}, {2}, "{3}")').format(userID, assignmentID, courseID, submissionInfo)
        db.session.execute(text(sql))
        db.session.commit()
        # get the submissionID
        sql = ('select submissionID '
                'from submission '
                'where userID = "{0}" and assignmentID = {1} and courseID = {2} and submissionInfo = "{3}"').format(userID, assignmentID, courseID, submissionInfo)
        data = db.session.execute(text(sql)).fetchall()
        submissionID = data[0][0]
        print('submissionID', submissionID)
        return jsonify({"status": "200", "msg": "修改成功", "submissionID": submissionID})
    
    else:
        return jsonify({"status": "1000", "msg": "method error"})


@app.route("/api/user/pwd_chg", methods=["POST"])
@cross_origin()
def user_pwd_chg():
    rq = request.json
    if request.method == 'POST':
        userID = rq.get('userID')
        password = rq.get('password')
        new_password = rq.get('new_password')
        sql = ('select * '
               + 'from user '
               + ' where userID = "{0}" and password = "{1}"').format(userID, password)
        data = db.session.execute(text(sql)).fetchall()
        if not data:
            return jsonify(status=1000, msg="原始密码错误")
        else:
            sql = ('update user set password = "{0}"'
                   + 'where userID = "{1}"').format(userID, new_password)
            db.session.execute(text(sql))
            db.session.commit()
            return jsonify(status=200, msg="修改成功")
