import { createRouter, createWebHistory } from 'vue-router';
import LogIn from '../components/LogIn.vue';
import Register from '../components/UserRegister.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import UserDashboard from '../components/UserDashboard.vue';
import TeacherCourse from '../components/TeacherCourse.vue';
import AdminCourse from "@/components/AdminCourse.vue";
import TeacherAssignment from '@/components/TeacherAssignment.vue';
import StudentCourse from '@/components/StudentCourse.vue';
import StudentAssignment from '@/components/StudentAssignment.vue';

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
    path: "/admin/course/:courseID",
    name: "AdminCourse",
    component: AdminCourse,
  },
  {
    path: '/teacher-course/:courseID/:userID',
    name: 'TeacherCourse',
    component: TeacherCourse,
  },
  {
    path: '/teacher/assignment/:courseID/:assignmentID',
    name: 'TeacherAssignment',
    component: TeacherAssignment,
    props: true
  },
  {
    path: '/student-course/:courseID/:userID',
    name: 'StudentCourse',
    component: StudentCourse,
  },
  {
    path: '/student/assignment/:courseID/:assignmentID/:userID',
    name: 'StudentAssignment',
    component: StudentAssignment,
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
