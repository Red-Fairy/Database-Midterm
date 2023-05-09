<template>
    <div class="student-dashboard">
      <h1>Student Dashboard</h1>
      <div class="course-list">
        <div class="course-item" v-for="course in courses" :key="course.courseID">
          <button @click="showHomework(course.courseID)">{{ course.courseInfo }}</button>
        </div>
      </div>
      <div v-if="selectedCourse">
        <h2>Homework for {{ selectedCourse.courseInfo }}</h2>
        <div class="homework-list">
          <div class="homework-item" v-for="homework in homeworkList" :key="homework.homeworkID">
            <span>{{ homework.homeworkInfo }}</span>
            <span v-if="homework.submitted">
              <span v-if="homework.grade">{{ homework.grade }}</span>
              <span v-else>Ungraded</span>
            </span>
            <span v-else>
              <button @click="submitHomework(homework.homeworkID)">Submit</button>
            </span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        courses: [], // Replace with actual data from API
        selectedCourse: null,
        homeworkList: [],
      };
    },
    methods: {
      // showHomework(courseID) {
      //   // Call the API to fetch homework for the selected course and update 'selectedCourse' and 'homeworkList'
      // },
      // submitHomework(homeworkID) {
      //   // Call the API to submit the homework
      // },
    },
  };
  </script>
  
  <style scoped>
  .course-list,
  .homework-list {
    display: flex;
    flex-direction: column;
  }
  </style>
  