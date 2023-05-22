<template>
    <div class="centered-container">
      <h1>{{ courseName }}</h1>
      <p>{{ courseInfo }}</p>
  
      <div v-if="error" class="error-message">{{ error }}</div>
  
      <h2>Teachers</h2>
      <table class="user-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>
              <div class="input-group">
                <input v-model="newTeacher" placeholder="Enter teacher username" class="input-field" />
                <button @click="addTeacher" class="add-button">Add</button>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(teacher, index) in teachers" :key="index">
            <td>{{ teacher }}</td>
            <td><button @click="deleteUser(teacher, true)">Delete</button></td>
          </tr>
        </tbody>
      </table>
  
      <h2>Students</h2>
      <table class="user-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>
              <div class="input-group">
                <input v-model="newStudent" placeholder="Enter student username" class="input-field" />
                <button @click="addStudent" class="add-button">Add</button>
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(student, index) in students" :key="index">
            <td>{{ student }}</td>
            <td><button @click="deleteUser(student, false)">Delete</button></td>
          </tr>
        </tbody>
      </table>
  
      <button>
        <router-link :to="{ name: 'AdminDashboard' }" class="button">返回主页</router-link>
      </button>
    </div>
  </template>
  
<script>
import api from "@/api.js";

export default {
    data() {
        return {
            teachers: [],
            students: [],
            newTeacher: "",
            newStudent: "",
            error: "",
            courseName: "",
            courseInfo: "",
        };
    },
    methods: {
        async getCourseData() {
            try {
                const response = await api.getCourseData(this.$route.params.courseID);
                if (response.data.status === "200") {
                    this.teachers = response.data.teachers;
                    this.students = response.data.students;
                    this.courseInfo = response.data.courseInfo;
                    this.courseName = response.data.courseName;
                } else {
                    console.error("Failed to fetch course data");
                }
            } catch (error) {
                console.error("Error fetching course data:", error);
            }
        },
        async addTeacher() {
            if (this.newTeacher) {
                const response = await api.addTeacher(this.$route.params.courseID, this.newTeacher);
                if (response.data.status === "200") {
                    this.teachers.push(this.newTeacher);
                    this.newTeacher = "";
                    this.error = "";
                } else {
                    this.error = response.data.msg;
                    this.newTeacher = "";
                }
            }
        },
        async addStudent() {
            if (this.newStudent) {
                const response = await api.addStudent(this.$route.params.courseID, this.newStudent);
                if (response.data.status === "200") {
                    this.students.push(this.newStudent);
                    this.newStudent = "";
                    this.error = "";
                } else {
                    this.error = response.data.msg;
                    this.newStudent = "";
                }
            }
        },
        async deleteUser(username, isTeacher) {
            console.log(this.$route.params.courseID, username, isTeacher);
            await api.deleteUser(this.$route.params.courseID, username);
            if (isTeacher) {
                this.teachers = this.teachers.filter((teacher) => teacher !== username);
            } else {
                this.students = this.students.filter((student) => student !== username);
            }
        },
    },
    async mounted() {
        await this.getCourseData();
    },
};
</script>
  
<style scoped>
.centered-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
}

p {
  margin-bottom: 20px;
  font-size: 16px;
}

.error-message {
  color: red;
  margin: 10px 0;
}

table.user-table {
  border-collapse: collapse;
  margin-bottom: 20px;
  width: 100%;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.input-group {
  display: flex;
  align-items: center;
}

.input-field {
  flex: 1;
  padding: 5px;
  font-size: 14px;
  width: 50%;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  box-sizing: border-box;
}

.add-button {
  margin-left: 8px;
  margin-top: 0;
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button {
  padding: 8px 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0px;
}
</style>

