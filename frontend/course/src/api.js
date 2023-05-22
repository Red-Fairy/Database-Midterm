/*
Author: Rundong Luo
E-mail: rundong_luo@stu.pku.edu.cn
*/

import axios from 'axios';

const api = axios.create({
  // local host
  baseURL: 'http://localhost:5000',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

export default {
  async register(username, password) {
    const response = await api.post('/api/user/register', {
      username,
      password,
    });
    return response.data;
  },

  async login(username, password) {
    const response = await api.post('/api/user/login', {
      userid: username,
      password: password,
    });
    return response.data;
  },

  async createCourse(course) {
    const response = await api.post("/api/user/course", {
      courseID: course.courseID,
      courseName: course.courseName,
      courseInfo: course.courseInfo,
      permission: true,
      method: "ADD",
    });
    return response.data;
  },
  async deleteCourse(courseID) {
    const response = await api.post("/api/user/course", {
      courseID: courseID,
      permission: true,
      method: "DELETE",
    });
    return response.data;
  },

  async getCourses(permission, userID) {
    const response = await api.get('/api/user/course', {
      params: {
        permission: permission,
        userID: userID,
      },
    });
    return response.data;
  },
  async getCourseData(courseID) {
    return await api.get("/api/user/user_course", {
      params: { courseID },
    });
  },
  async addTeacher(courseID, userID) {
    return await api.post("/api/user/user_course", {
      method: "ADD",
      permission: true,
      courseID,
      userID,
      teacher: 1,
    });
  },
  async addStudent(courseID, userID) {
    return await api.post("/api/user/user_course", {
      method: "ADD",
      permission: true,
      courseID,
      userID,
      teacher: 0,
    });
  },
  async deleteUser(courseID, userID) {
    return await api.post("/api/user/user_course", {
      method: "DELETE",
      permission: true,
      courseID,
      userID,
    });
  },
  async getCourseLectures(courseID) {
    const response = await api.get("/api/user/lecture", {
      params: { courseID },
    });
    return response.data;
  },

  async addCourseLecture(lectureInfo) {
    lectureInfo.permission = true;
    const response = await api.post('/api/user/lecture', lectureInfo);
    return response.data;
  },

  async updateCourseLecture(lectureInfo) {
    lectureInfo.permission = true;
    const response = await api.post('/api/user/lecture', lectureInfo);
    return response.data;
  },
  async getCourseAssignments(courseID) {
    const response = await api.get(`/api/user/assignment?courseID=${courseID}`);
    return response.data;
  },

  async addCourseAssignment(assignmentInfo) {
    const response = await api.post('/api/user/assignment', assignmentInfo);
    return response.data;
  },

  async updateCourseAssignment(assignmentInfo) {
    const response = await api.post('/api/user/assignment', assignmentInfo);
    return response.data;
  },
  async getCourseAssignmentSubmissions(courseID, assignmentID, permission) {
    // use post method, add a permission field to the request body
    const info = {
      courseID: courseID,
      assignmentID: assignmentID,
      permission: permission,
      method: 'GET',
    };
    console.log(info);
    const response = await api.post('/api/user/submission', info);
    return response.data;
  },
  async updateSubmissionScore(submissionID, score) {
    const info = {
      submissionID: submissionID,
      score: score,
      permission: true,
      method: 'UPDATE',
    };
    console.log(info);
    const response = await api.post('/api/user/submission', info);
    return response.data;
  },
  async getCourseAssignmentSubmissionsStudent(courseID, assignmentID, userID, permission) {
    // use post method, add a permission field to the request body
    const info = {
      courseID: courseID,
      assignmentID: assignmentID,
      userID: userID,
      permission: permission,
      method: 'GET',
    };
    const response = await api.post('/api/user/submission', info);
    return response.data;
  },
  async submitAssignment(assignmentID, courseID, userID, submissionInfo) {
    const info = {
      courseID: courseID,
      assignmentID: assignmentID,
      userID: userID,
      submissionInfo: submissionInfo,
      permission: true,
      method: 'SUBMIT',
    };
    const response = await api.post('/api/user/submission', info);
    return response.data;
  }
};
