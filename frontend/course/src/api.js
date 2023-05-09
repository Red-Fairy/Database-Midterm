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
  // 在此处添加其他API请求方法
};
