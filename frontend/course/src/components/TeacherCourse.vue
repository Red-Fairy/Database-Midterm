<template>
    <div>
        <h3>课程名称：{{ courseName }}</h3>
        <h3>课程信息：{{ courseInfo }}</h3>
        <h3>教师列表：</h3>
        <table>
            <thead>
                <tr>
                    <th>教师ID</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="teacher in teachers" :key="teacher">
                    <td>{{ teacher }}</td>
                </tr>
            </tbody>
        </table>
        <h3>学生列表：</h3>
        <table>
            <thead>
                <tr>
                    <th>学生ID</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="student in students" :key="student">
                    <td>{{ student }}</td>
                </tr>
            </tbody>
        </table>

        <h3>讲座信息：</h3>
        <table>
            <thead>
                <tr>
                    <th>讲座ID</th>
                    <th>讲座信息</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="lecture in lectures" :key="lecture.lectureID">
                    <td>{{ lecture.lectureID }}</td>
                    <td>
                        <input v-model="editLectureInfo[lecture.lectureID]" type="text"
                            :placeholder="lecture.lectureInfo" />
                    </td>
                    <td>
                        <button @click="editLecture(lecture.lectureID)">编辑</button>
                        <button @click="deleteLecture(lecture.lectureID)">删除</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <input v-model="newLectureInfo.lectureID" type="int" placeholder="输入新的讲座ID" />
        <input v-model="newLectureInfo.lectureInfo" type="text" placeholder="输入新的讲座信息" />
        <button @click="addLecture">添加讲座</button>

        <h3>作业信息：</h3>
        <table>
            <thead>
                <tr>
                    <th>作业ID</th>
                    <th>作业信息</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="assignment in assignments" :key="assignment.assignmentID">
                    <td>{{ assignment.assignmentID }}</td>
                    <td>
                        <input v-model="editAssignmentInfo[assignment.assignmentID]" type="text"
                            :placeholder="assignment.assignmentInfo" />
                    </td>
                    <td>
                        <button @click="editAssignment(assignment.assignmentID)">编辑</button>
                        <button @click="deleteAssignment(assignment.assignmentID)">删除</button>
                        <button @click="goToAssignment(assignment.assignmentID, courseID)">查看作业</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <input v-model="newAssignmentInfo.assignmentID" type="int" placeholder="输入新的作业ID" />
        <input v-model="newAssignmentInfo.assignmentInfo" type="text" placeholder="输入新的作业信息" />
        <button @click="addAssignment">添加作业</button>
    </div>
</template>
  
<script>
import api from '@/api.js';

export default {
    data() {
        return {
            courseID: '',
            userID: '',
            students: [],
            teachers: [],
            lectures: [],
            assignments: [],
            courseInfo: '',
            courseName: '',
            newLectureInfo: {
                lectureID: '',
                lectureInfo: '',
            },
            newAssignmentInfo: {
                assignmentID: '',
                assignmentInfo: '',
            },
            editLectureInfo: {},
            editAssignmentInfo: {},
        };
    },

    async mounted() {
        this.userID = this.$route.params.userID;
        this.courseID = this.$route.params.courseID;
        const courseID = this.$route.params.courseID;
        const response = await api.getCourseData(courseID);
        if (response.data.status === "200") {
            this.students = response.data.students;
            this.teachers = response.data.teachers;
            this.courseInfo = response.data.courseInfo;
            this.courseName = response.data.courseName;
        } else {
            console.error("Failed to fetch course data");
        }

        const lecturesInfo = await api.getCourseLectures(courseID);
        this.lectures = lecturesInfo.tabledata;

        const assignmentsInfo = await api.getCourseAssignments(courseID);
        this.assignments = assignmentsInfo.tabledata;
    },

    methods: {
        async editLecture(lectureID) {
            const lectureInfo = this.editLectureInfo[lectureID];
            const courseID = this.$route.params.courseID;
            if (lectureInfo) {
                await api.updateCourseLecture({
                    courseID: courseID,
                    lectureID: lectureID,
                    lectureInfo: lectureInfo,
                    method: 'UPDATE',
                });
                this.lectures = this.lectures.map(lecture =>
                    lecture.lectureID === lectureID
                        ? { ...lecture, lectureInfo }
                        : lecture
                );
            }
        },
        async addLecture() {
            const lectureInfo = this.newLectureInfo;
            if (lectureInfo) {
                lectureInfo['method'] = 'ADD';
                lectureInfo['courseID'] = this.$route.params.courseID;
                const response = await api.addCourseLecture(lectureInfo);
                // update the lecture table
                if (response.status === "200") {
                    this.lectures.push({
                        lectureID: lectureInfo.lectureID,
                        lectureInfo: lectureInfo.lectureInfo,
                    });
                    this.newLectureInfo = '';
                } else {
                    console.error("Failed to add lecture");
                }
            }
        },
        async deleteLecture(lectureID) {
            const courseID = this.$route.params.courseID;
            await api.updateCourseLecture({
                courseID: courseID,
                lectureID: lectureID,
                method: 'DELETE',
            });
            this.lectures = this.lectures.filter(lecture => lecture.lectureID !== lectureID);
        },
        async editAssignment(assignmentID) {
            const assignmentInfo = this.editAssignmentInfo[assignmentID];
            if (assignmentInfo) {
                await api.updateCourseAssignment({
                    courseID: this.$route.params.courseID,
                    assignmentID: assignmentID,
                    assignmentInfo: assignmentInfo,
                    method: 'UPDATE',
                });
                this.assignments = this.assignments.map(assignment =>
                    assignment.assignmentID === assignmentID
                        ? { ...assignment, assignmentInfo }
                        : assignment
                );
            }
        },
        async addAssignment() {
            const assignmentInfo = this.newAssignmentInfo;
            if (assignmentInfo) {
                assignmentInfo['method'] = 'ADD';
                assignmentInfo['courseID'] = this.$route.params.courseID;
                const response = await api.addCourseAssignment(assignmentInfo);
                if (response.status === "200") {
                    this.assignments.push({
                        assignmentID: assignmentInfo.assignmentID,
                        assignmentInfo: assignmentInfo.assignmentInfo,
                    });
                    this.newAssignmentInfo = '';
                } else {
                    console.error("Failed to add assignment");
                }
            }
        },
        async deleteAssignment(assignmentID) {
            await api.updateCourseAssignment({
                courseID: this.$route.params.courseID,
                assignmentID: assignmentID,
                method: 'DELETE',
            });
            this.assignments = this.assignments.filter(assignment => assignment.assignmentID !== assignmentID);
        },
        goToAssignment(assignmentID, courseID) {
            this.$router.push({ name: 'TeacherAssignment', params: { assignmentID, courseID } });
        },
    },
};
</script>

  