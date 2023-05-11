/*
* Author: Yuyang Zhou
* Email: 2000013061@stu.pku.edu.cn
*/

/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/5/2 12:42:35                            */
/*==============================================================*/
drop database if exists tlatpku;

create database tlatpku;

use tlatpku;

drop table if exists course;

drop table if exists assignment;

drop table if exists lecture;

drop table if exists submission;

drop table if exists teacher;

drop table if exists user;

drop table if exists userCourseRelationship;

/*==============================================================*/
/* Table: course                                                */
/*==============================================================*/
create table course
(
   courseID             int not null,
   courseName            char(128) not null,
   courseInfo           char(128),
   primary key (courseID)
);

INSERT INTO course VALUES (1, '编译原理', '编译原理是四大礼包中的一门课');
INSERT INTO course VALUES (2, '数据库导论', '数据库导论不是四大礼包中的一门课');

/*==============================================================*/
/* Table: assignment                                              */
/*==============================================================*/
create table assignment
(
   assignmentID           int not null,
   courseID             int not null,
   assignmentInfo         char(128),
   primary key (assignmentID, courseID)
);

INSERT INTO assignment VALUES (1, 1, '数据库导论期中大作业');
INSERT INTO assignment VALUES (2, 2, '编译原理Sysy编译器作业');

/*==============================================================*/
/* Table: lecture                                               */
/*==============================================================*/
create table lecture
(
   lectureID            int AUTO_INCREMENT,
   courseID             int not null,
   lectureInfo          char(128),
   primary key (lectureID, courseID)
);

INSERT INTO lecture (courseID, lectureInfo) VALUES (1, '初级SQL语言');
INSERT INTO lecture (courseID, lectureInfo) VALUES (1, '高级SQL语言');
INSERT INTO lecture (courseID, lectureInfo) VALUES (1, 'ER图设计');

/*==============================================================*/
/* Table: submission                                            */
/*==============================================================*/
create table submission
(
   submissionID         int AUTO_INCREMENT,
   userID               char(128) not null,
   assignmentID           int not null,
   courseID				int not null,
   submissionInfo       char(128) not null,
   submissionScore      decimal(8),
   primary key (submissionID)
);

INSERT INTO submission VALUES (1, 'redfairy', 1, 1, '你盯着垃圾桶看了许久，但这还是平平无奇的垃圾桶。', null);
INSERT INTO submission VALUES (2, 'redfairy', 1, 1, '你盯着垃圾桶看了许久，他们好像变了，寒铁桶便不再锈迹斑斑，桶身上的凹陷也平整了许多。', null);
INSERT INTO submission VALUES (3, 'redfairy', 1, 1, '从垃圾桶盖下微微透出金色的光芒--甜蜜而诱人，有一瞬间，你甚至觉得垃圾桶变成了宝箱。', null);
INSERT INTO submission VALUES (4, 'redfairy', 1, 1, '你深吸一口气，伸出手，掀开桶盖：里面什么也没有。', null);
INSERT INTO submission VALUES (5, 'redfairy', 1, 1, '不对，你弯腰把手伸进垃圾桶里，从桶底捡起一块铁片。功夫不负有心人，你终于找到了宝藏！', null);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   userID               char(128) not null,
   password             char(128) not null,
   superManager         bool not null,
   primary key (userID)
);

INSERT INTO user VALUES ('redfairy', 'redfairy', True);
INSERT INTO user VALUES ('bluefairy', 'bluefairy', false);
INSERT INTO user VALUES ('yellowfairy', 'yellowfairy', false);

/*==============================================================*/
/* Table: userCourseRelationship                                */
/*==============================================================*/
create table userCourseRelationship
(
   courseID             int not null,
   userID               char(128) not null,
   teacher              bool not null,
   primary key (courseID, userID)
);

INSERT INTO userCourseRelationship VALUES (1, 'redfairy', false);
INSERT INTO userCourseRelationship VALUES (1, 'bluefairy', true);
INSERT INTO userCourseRelationship VALUES (1, 'yellowfairy', false);

alter table assignment add constraint FK_courseOfassignment foreign key (courseID)
      references course (courseID) on delete cascade on update cascade;

alter table lecture add constraint FK_courseOfLecture foreign key (courseID)
      references course (courseID) on delete cascade on update cascade;

alter table submission add constraint FK_assignmentOfSubmission foreign key (assignmentID)
      references assignment (assignmentID) on delete cascade on update cascade;

alter table submission add constraint FK_userOfSubmission foreign key (userID)
      references user (userID) on delete cascade on update cascade;

alter table userCourseRelationship add constraint FK_courseOfRelationship foreign key (courseID)
      references course (courseID) on delete cascade on update cascade;

alter table userCourseRelationship add constraint FK_userOfRelationship foreign key (userID)
      references user (userID) on delete cascade on update cascade;

/*
testing code:

use tlatpku;

select * from submission;

use tlatpku;

delete from assignment
where assignmentID = 1;

select * from submission;
*/

