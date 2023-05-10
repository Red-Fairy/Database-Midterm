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

  async getCourses(permission) {
    const response = await api.get('/api/user/course', {
      params: {
        permission: permission,
      },
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
    const response = await api.delete("/api/user/course", {
      data: {
        courseID: courseID,
        permission: true,
      },
    });
    return response.data;
  },



  // Add other API functions if needed
};
