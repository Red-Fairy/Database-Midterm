<template>
    <div class="teacher-dashboard">
      <h1>Teacher Dashboard</h1>
      <div class="course-list">
        <div class="course-item" v-for="course in courses" :key="course.courseID">
          <button @click="showHomework(course.courseID)">{{ course.courseInfo }}</button>
        </div>
      </div>
      <div v-if="selectedCourse">
        <h2>Homework for {{ selectedCourse.courseInfo }}</h2>
        <div class="homework-list">
          <div class="homework-item" v-for="homework in homeworkList" :key="homework.homeworkID">
            <button @click="showSubmissions(homework.homeworkID)">{{ homework.homeworkInfo }}</button>
          </div>
        </div>
      </div>
      <div v-if="selectedHomework">
        <h2>Submissions for {{ selectedHomework.homeworkInfo }}</h2>
        <div class="submissions-list">
          <div class="submission-item" v-for="submission in submissions" :key="submission.submissionID">
            <span>{{ submission.studentName }}</span>
            <input v-model="submission.grade" placeholder="Grade" />
          <button @click="gradeSubmission(submission.submissionID)">Grade</button>
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
      selectedHomework: null,
      submissions: [],
    };
  },
  methods: {
    // showHomework(courseID) {
    //   // Call the API to fetch homework for the selected course and update 'selectedCourse' and 'homeworkList'
    // },
    // showSubmissions(homeworkID) {
    //   // Call the API to fetch submissions for the selected homework and update 'selectedHomework' and 'submissions'
    // },
    // gradeSubmission(submissionID) {
    //   // Call the API to grade the submission
    // },
  },
};
</script>

<style scoped>
.course-list,
.homework-list,
.submissions-list {
  display: flex;
  flex-direction: column;
}
</style>

  