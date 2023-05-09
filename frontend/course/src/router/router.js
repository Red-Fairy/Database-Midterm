import { createRouter, createWebHistory } from 'vue-router';
import LogIn from '../components/LogIn.vue';
import Register from '../components/UserRegister.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import UserDashboard from '../components/UserDashboard.vue';
import CourseDashboard from '../components/CourseDashboard.vue';

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'LogIn',
    component: LogIn,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },
  {
    path: '/user-dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
  },
  {
    path: '/course',
    name: 'CourseDashboard',
    component: CourseDashboard,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
