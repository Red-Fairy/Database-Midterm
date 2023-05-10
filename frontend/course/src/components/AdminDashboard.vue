<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <form @submit.prevent="createCourse">
      <div>
        <label for="courseID">Course ID:</label>
        <input type="text" id="courseID" v-model="courseID" />
      </div>
      <div>
        <label for="courseInfo">Course Name:</label>
        <input type="text" id="courseInfo" v-model="courseInfo" />
      </div>
      <div>
        <button type="submit">Create Course</button>
      </div>
    </form>
    <table>
      <thead>
        <tr>
          <th>Course ID</th>
          <th>Course Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.courseID">
          <td>{{ course.courseID }}</td>
          <td>
            <router-link :to="{ name: 'CourseDashboard', params: { courseID: course.courseID } }">
              {{ course.courseInfo }}
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      courses: [],
    };
  },
  async created() {
    try {
      const response = await api.getCourses(/* provide necessary parameters here */);
      if (response.status === '200') {
        this.courses = response.tabledata;
      } else {
        // Handle error case
      }
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  },
};
</script>
