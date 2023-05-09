import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api', // Replace this with your actual API base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
