<template>
    <div class="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <div>
        <button @click="createCourse">Create Course</button>
      </div>
      <div class="course-list">
        <div class="course-item" v-for="course in courses" :key="course.courseID">
          <span>{{ course.courseInfo }}</span>
          <button @click="editCourse(course.courseID)">Edit</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        courses: [], // Replace with actual data from API
      };
    },
    methods: {
      createCourse() {
        // Call the create course API
      },
      // editCourse(courseID) {
      //   // Call the edit course API
      // },
    },
  };
  </script>
  
  <style scoped>
  .course-list {
    display: flex;
    flex-direction: column;
  }
  </style>
  