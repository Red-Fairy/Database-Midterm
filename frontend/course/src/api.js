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

  async getCourses(permission, userID) {
    try {
      const response = await api.get('/api/user/course', {
        params: {
          permission,
          userID,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching courses:', error);
      throw error;
    }
  },

  async getCourseData(courseID /* Add other necessary parameters */) {
    try {
      // Implement the actual API call here according to your API's requirements
      // For example:
      const response = await api.get('/api/user/course_data', {
        params: {
          courseID,
          // Add other necessary parameters
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching course data:', error);
      throw error;
    }
  },
  async addCourse(courseID, courseInfo) {
    try {
      const response = await api.post('/api/user/course', {
        method: "ADD",
        permission: true, // Assuming the user has permission
        courseID,
        courseInfo,
      });
      return response.data;
    } catch (error) {
      console.error('Error adding course:', error);
      throw error;
    }
  },
  async getCourseUsers(courseID) {
    try {
      const response = await api.get('/api/user/user_course', {
        params: {
          courseID,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching course users:', error);
      throw error;
    }
  },
  
  async updateUserCourseRelation(method, courseID, userID, teacher) {
    try {
      const response = await api.post('/api/user/user_course', {
        method,
        permission: true, // Assuming the user has permission
        courseID,
        userID,
        teacher,
      });
      return response.data;
    } catch (error) {
      console.error('Error updating user-course relation:', error);
      throw error;
    }
  },
  
  
  // Add other API functions if needed
};
