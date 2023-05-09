import axios from 'axios';

const apiClient = axios.create({
  // local host
  baseURL: 'http://localhost:5000',
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

export default {
  async register(username, password) {
    const response = await apiClient.post('/api/user/register', {
      username,
      password,
    });
    return response.data;
  },
  // 在此处添加其他API请求方法
};
