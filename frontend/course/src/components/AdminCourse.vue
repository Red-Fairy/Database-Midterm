<template>
    <div>
        <h1>{{ courseName }}</h1>
        <p>{{ courseInfo }}</p>
        <div v-if="error" class="error">{{ error }}</div>
        <h2>Teachers</h2>
        <table>
            <thead>
                <tr>
                    <th>Username</th>
                    <th>
                        <input v-model="newTeacher" />
                        <button @click="addTeacher">Add</button>
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
        <table>
            <thead>
                <tr>
                    <th>Username</th>
                    <th>
                        <input v-model="newStudent" />
                        <button @click="addStudent">Add</button>
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
                } else {
                    this.error = "Failed to add teacher"
                }
            }
        },
        async addStudent() {
            if (this.newStudent) {
                const response = await api.addStudent(this.$route.params.courseID, this.newStudent);
                if (response.data.status === "200") {
                    this.students.push(this.newStudent);
                    this.newStudent = "";
                } else {
                    this.error = "Failed to add student"
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
table {
    border-collapse: collapse;
    margin-bottom: 20px;
}

th,
td {
    border: 1px solid black;
    padding: 5px;
}
</style>
  