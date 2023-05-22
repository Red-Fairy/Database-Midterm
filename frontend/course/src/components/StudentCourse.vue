<template>
  <div class="course-details">
    <div>
      <button>
        <router-link :to="{ name: 'UserDashboard' }" class="button">返回主页</router-link>
      </button>
    </div>
    <h3>课程名称：{{ courseName }}</h3>
    <h3>课程信息：{{ courseInfo }}</h3>

    <div class="teacher-list">
      <h3>教师列表：</h3>
      <table>
        <thead>
          <tr>
            <th class="centered-header">教师ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="teacher in teachers" :key="teacher">
            <td>{{ teacher }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="student-list">
      <h3>学生列表：</h3>
      <table>
        <thead>
          <tr>
            <th class="centered-header">学生ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student">
            <td>{{ student }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="lecture-list">
      <h3>讲座信息：</h3>
      <table>
        <thead>
          <tr>
            <th class="centered-header">讲座ID</th>
            <th class="centered-header">讲座信息</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lecture in lectures" :key="lecture.lectureID">
            <td>{{ lecture.lectureID }}</td>
            <td>{{ lecture.lectureInfo }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="assignment-list">
      <h3>作业信息：</h3>
      <table>
        <thead>
          <tr>
            <th class="centered-header">作业ID</th>
            <th class="centered-header">作业信息</th>
            <th class="centered-header">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="assignment in assignments" :key="assignment.assignmentID">
            <td>{{ assignment.assignmentID }}</td>
            <td>{{ assignment.assignmentInfo }}</td>
            <td>
              <button @click="goToAssignment(userID, courseID, assignment.assignmentID)">查看作业</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
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
    goToAssignment(userID, courseID, assignmentID) {
      this.$router.push({ name: 'StudentAssignment', params: { userID, courseID, assignmentID } });
    },
  },
};
</script>

<style scoped>
.course-details {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.course-details h3 {
  margin: 10px 0;
}

.course-details table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.course-details th,
.course-details td {
  padding: 8px;
  border: 1px solid #ddd;
}

.course-details .centered-header {
  text-align: center;
}

.course-details button {
  padding: 6px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.course-details button:not(:last-child) {
  margin-right: 5px;
}
</style>