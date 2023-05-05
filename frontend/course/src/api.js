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
  getTables() {
    return apiClient.get('/tables');
  },
  getTable(id) {
    return apiClient.get(`/tables/${id}`);
  },
  login(username, password) {
    return apiClient.post('/login', { username, password });
  },
  // Add other API methods as needed
};
