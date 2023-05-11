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
                </tr>
            </thead>
            <tbody>
                <tr v-for="lecture in lectures" :key="lecture.lectureID">
                    <td>{{ lecture.lectureID }}</td>
                    <td>{{ lecture.lectureInfo }}</td>
                </tr>
            </tbody>
        </table>

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
                        {{ assignment.assignmentInfo }}
                    </td>
                    <td>
                        <button @click="goToAssignment(assignment.assignmentID, courseID, userID)">查看作业</button>
                    </td>
                </tr>
            </tbody>
        </table>
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
            Teachers: [],
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
        goToAssignment(assignmentID, courseID, userID) {
            this.$router.push({ name: 'StudentAssignment', params: { assignmentID, courseID, userID } });
        },
    },
};
</script>

  