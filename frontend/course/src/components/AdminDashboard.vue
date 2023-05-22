<template>
  <div class="centered-container">
    <h2>课程管理</h2>
    <table class="course-table">
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
            <button @click="deleteCourse(course.courseID)" class="delete-button">删除课程</button>
            <button class="enter-button">
              <router-link :to="{
                name: 'AdminCourse',
                params: { courseID: course.courseID },
              }" class="enter-link">
                进入课程
              </router-link>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="new-course-form">
      <h3>创建新课程</h3>
      <input v-model="newCourse.courseID" placeholder="课程ID" class="input-field" />
      <input v-model="newCourse.courseName" placeholder="课程名称" class="input-field" />
      <input v-model="newCourse.courseInfo" placeholder="课程信息" class="input-field" />
      <button @click="createCourse" class="create-button">创建课程</button>
    </div>
    <div v-if="error" class="error-message">{{ error }}</div>
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
          this.error = "课程创建成功"; // 清除错误
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

<style scoped>
table.course-table {
  margin-top: 5px;
  border-collapse: collapse;
  width: 100%;
}

table.course-table th,
table.course-table td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

table.course-table th {
  background-color: #f2f2f2;
}

.button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.enter-button {
  background-color: #2196f3;
  color: white;
}

.input-field {
  padding: 8px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}

.create-button {
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>