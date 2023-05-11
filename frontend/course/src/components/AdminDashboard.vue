<template>
  <div>
    <h2>课程管理</h2>
    <div class="new-course-form">
      <h3>创建新课程</h3>
      <input v-model="newCourse.courseID" placeholder="课程ID" />
      <input v-model="newCourse.courseName" placeholder="课程名称" />
      <input v-model="newCourse.courseInfo" placeholder="课程信息" />
      <button @click="createCourse">创建课程</button>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <table>
      <thead>
        <tr>
          <th>课程ID</th>
          <th>课程名称</th>
          <th>课程信息</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.courseID">
          <td>{{ course.courseID }}</td>
          <td>{{ course.courseName }}</td>
          <td>{{ course.courseInfo }}</td>
          <td>
            <button @click="deleteCourse(course.courseID)">删除课程</button>
            <button>
              <router-link :to="{
                name: 'AdminCourse',
                params: { courseID: course.courseID },
              }" class="btn btn-default">
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
  data() {
    return {
      newCourse: {
        courseID: "",
        courseName: "",
        courseInfo: "",
      },
      courses: [],
      error: "", // 添加这一行
    };
  },
  methods: {
    async createCourse() {
      if (
        this.newCourse.courseID &&
        this.newCourse.courseName &&
        this.newCourse.courseInfo
      ) {
        const response = await api.createCourse(this.newCourse);
        if (response.status === "200") {
          this.courses.push(this.newCourse);
          this.newCourse = {
            courseID: "",
            courseName: "",
            courseInfo: "",
          };
          this.error = ""; // 清除错误
        } else {
          this.error = "创建课程失败";
        }
      }
    },
    async deleteCourse(courseID) {
      if (confirm("确定要删除这个课程吗？")) {
        const response = await api.deleteCourse(courseID);
        if (response.status === "200") {
          this.courses = this.courses.filter((course) => course.courseID !== courseID);
          this.error = ""; // 清除错误
        } else {
          this.error = "删除课程失败";
        }
      }
    },
  },
  async mounted() {
    const response = await api.getCourses('admin');
    if (response.status === "200") {
      this.courses = response.tabledata;
    } else {
      // Handle error
    }
  },
};
</script>

