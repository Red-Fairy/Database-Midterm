### Install redis(WSL):

```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```

### Launch redis(WSL)

```bash
sudo service redis-server start
```

### Connection test

```bash
redis-cli
127.0.0.1:6379> ping
PONG
```

### 一些关于访问权限的问题

目前没有实现检查用户是否能够访问作业所属的课程的接口。

权限系统大概分成这几档：

超管：记录在 user 表中，能够编辑课程，编辑用户课程关系，查看所有课时，作业的信息

教师：记录在 userCourseRelationship，能够在自己担任教师的课程中编辑课时与作业，同时给该课时的作业提交打分

学生：记录在 userCourseRelationship，能够在自己担任学生的课程中查看课时与作业，同时提交该课时的作业