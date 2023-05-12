<template>
  <div class="centered-container">
    <h3 class="section-title">以下课程中，您为学生：</h3>
    <table class="course-table">
      <thead>
        <tr>
          <th>课程ID</th>
          <th>课程名称</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in student_courses" :key="course.courseID">
          <td>{{ course.courseID }}</td>
          <td>{{ course.courseName }}</td>
          <td>
            <button class="action-button">
              <router-link :to="{ name: 'StudentCourse', params: { courseID: course.courseID, userID: userID } }">
                进入课程
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h3 class="section-title">以下课程中，您为老师：</h3>
    <table class="course-table">
      <thead>
        <tr>
          <th>课程ID</th>
          <th>课程名称</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in teacher_courses" :key="course.courseID">
          <td>{{ course.courseID }}</td>
          <td>{{ course.courseName }}</td>
          <td>
            <button class="action-button">
              <router-link :to="{ name: 'TeacherCourse', params: { courseID: course.courseID, userID: userID } }">
                进入课程
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

  
<script>
import api from "@/api.js";

export default {
  name: 'ComponentName',
  data() {
    return {
      userID: '',
      error: '',
      student_courses: [],
      teacher_courses: [],
    };
  },
  async mounted() {
    const userID = localStorage.getItem('userID'); // 从 localStorage 获取 userID
    this.userID = userID;
    const response = await api.getCourses('user', userID);
    if (response.status === "200") {
      this.student_courses = response.student_courses;
      this.teacher_courses = response.teacher_courses;
    } else {
      // Handle error
    }
  },
  methods: {
    // Your component methods go here
  },
};
</script>
  
<style scoped>
.error {
  color: red;
}

.centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: 20px;
  margin-bottom: 10px;
}

.course-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.course-table th,
.course-table td {
  padding: 8px;
  border: 1px solid #ddd;
}

.course-table th {
  background-color: #f5f5f5;
  font-weight: bold;
  text-align: left;
}

.course-table .action-button {
  padding: 6px 12px;
  background-color: #ffffff;
  color: rgb(1, 1, 1);
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.course-table .action-button:hover {
  background-color: #315bce9f;
}

</style>