<template>
  <div>
    <h3>以下课程中，您为学生：</h3>
    <table>
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
            <button>
              <router-link :to="{ name: 'CourseDashboard', params: { courseID: course.courseID } }">
                进入课程
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h3>以下课程中，您为老师：</h3>
    <table>
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
            <button>
              <router-link :to="{ name: 'CourseDashboard', params: { courseID: course.courseID } }">
                进入课程
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

  
<script>
import api from "@/api.js";

export default {
  name: 'ComponentName',
  data() {
    return {
      student_courses: [],
      teacher_courses: [],
    };
  },
  async mounted() {
    const userID = localStorage.getItem('userID'); // 从 localStorage 获取 userID
    console.log(userID);
    const response = await api.getCourses('user', userID);
    if (response.status === "200") {
      console.log(response.student_courses);
      console.log(response.teacher_courses);
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
/* Your component styles go here */
</style>