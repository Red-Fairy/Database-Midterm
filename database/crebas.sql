/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2023/5/2 12:42:35                            */
/*==============================================================*/


drop table if exists course;

drop table if exists homework;

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
   courseID             char(256) not null,
   courseInfo           char(256),
   primary key (courseID)
);

INSERT INTO course VALUES ('编译原理', '编译原理是四大礼包中的一门课');
INSERT INTO course VALUES ('数据库导论', '数据库导论不是四大礼包中的一门课');

/*==============================================================*/
/* Table: homework                                              */
/*==============================================================*/
create table homework
(
   homeworkID           int not null,
   courseID             char(256) not null,
   homeworkInfo         char(256),
   primary key (homeworkID)
);

INSERT INTO homework VALUES (1, '数据库导论', '数据库导论期中大作业');
INSERT INTO homework VALUES (2, '编译原理', '编译原理Sysy编译器作业');

/*==============================================================*/
/* Table: lecture                                               */
/*==============================================================*/
create table lecture
(
   lectureID            int not null,
   courseID             char(256) not null,
   lectureInfo          char(256),
   primary key (lectureID)
);

INSERT INTO lecture VALUES (1, '数据库导论', '初级SQL语言');
INSERT INTO lecture VALUES (2, '数据库导论', '高级SQL语言');
INSERT INTO lecture VALUES (3, '数据库导论', 'ER图设计');

/*==============================================================*/
/* Table: submission                                            */
/*==============================================================*/
create table submission
(
   submissionID         int not null,
   userID               char(256) not null,
   homeworkID           int not null,
   submissionInfo       char(256) not null,
   submissionScore      decimal(8),
   primary key (submissionID)
);

INSERT INTO submission VALUES (1, 'redfairy', 1, '你盯着垃圾桶看了许久，但这还是平平无奇的垃圾桶。', null);
INSERT INTO submission VALUES (2, 'redfairy', 1, '你盯着垃圾桶看了许久，他们好像变了，寒铁桶便不再锈迹斑斑，桶身上的凹陷也平整了许多。', null);
INSERT INTO submission VALUES (3, 'redfairy', 1, '从垃圾桶盖下微微透出金色的光芒--甜蜜而诱人，有一瞬间，你甚至觉得垃圾桶变成了宝箱。', null);
INSERT INTO submission VALUES (4, 'redfairy', 1, '你深吸一口气，伸出手，掀开桶盖：里面什么也没有。', null);
INSERT INTO submission VALUES (5, 'redfairy', 1, '不对，你弯腰把手伸进垃圾桶里，从桶底捡起一块铁片。功夫不负有心人，你终于找到了宝藏！', null);

/*==============================================================*/
/* Table: teacher                                               */
/*==============================================================*/
create table teacher
(
   teacher              bool not null,
   relationID           int not null,
   primary key (teacher)
);

INSERT INTO user VALUES (True, 1);
INSERT INTO user VALUES (False, 2);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   userID               char(256) not null,
   password             char(256) not null,
   primary key (userID)
);

INSERT INTO user VALUES ('redfairy', 'redfairy');
INSERT INTO user VALUES ('bluefairy', 'bluefairy');

/*==============================================================*/
/* Table: userCourseRelationship                                */
/*==============================================================*/
create table userCourseRelationship
(
   relationID           int not null,
   courseID             char(256) not null,
   userID               char(256) not null,
   primary key (relationID)
);


INSERT INTO user VALUES ('redfairy', '数据库原理', 2;
INSERT INTO user VALUES ('bluefairy', '数据库原理', 1);

alter table homework add constraint FK_courseOfHomework foreign key (courseID)
      references course (courseID) on delete restrict on update restrict;

alter table lecture add constraint FK_courseOfLecture foreign key (courseID)
      references course (courseID) on delete restrict on update restrict;

alter table submission add constraint FK_homeworkOfSubmission foreign key (homeworkID)
      references homework (homeworkID) on delete restrict on update restrict;

alter table submission add constraint FK_userOfSubmission foreign key (userID)
      references user (userID) on delete restrict on update restrict;

alter table teacher add constraint FK_userCourseRelationshipType foreign key (relationID)
      references userCourseRelationship (relationID) on delete restrict on update restrict;

alter table userCourseRelationship add constraint FK_courseOfRelationship foreign key (courseID)
      references course (courseID) on delete restrict on update restrict;

alter table userCourseRelationship add constraint FK_userOfRelationship foreign key (userID)
      references user (userID) on delete restrict on update restrict;
