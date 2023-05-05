// import Vue from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

// import TableList from './components/TableList.vue';
// import TableItem from './components/TableItem.vue';

// export default new Router({
//   mode: 'history',
//   routes: [
//     {
//       path: '/',
//       name: 'table-list',
//       component: TableList,
//     },
//     {
//       path: '/table/:id',
//       name: 'table-item',
//       component: TableItem,
//     },
//   ],
// });

import LogIn from './components/LogIn.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import UserDashboard from './components/UserDashboard.vue';

const routes = [
    {
        path: '/',
        redirect: '/logIn', // or any other route you'd like to use as the default
    },
    {
        path: '/logIn',
        name: 'logIn',
        component: LogIn,
    },
    {
        path: '/admin',
        name: 'admin',
        component: AdminDashboard,
        meta: {
            requiresAuth: true,
            allowedRoles: ['admin'],
        },
    },
    {
        path: '/user',
        name: 'user',
        component: UserDashboard,
        meta: {
            requiresAuth: true,
            allowedRoles: ['user'],
        },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
    const userRole = localStorage.getItem('userRole');
    const accessToken = localStorage.getItem('accessToken');

    if (requiresAuth && !accessToken) {
        // Redirect to the login page if the route requires authentication and there's no access token
        next({ name: 'login' });
    } else if (to.meta.allowedRoles && !to.meta.allowedRoles.includes(userRole)) {
        // Redirect to a 'not authorized' or 'forbidden' page if the user's role is not allowed for the route
        next({ name: 'forbidden' });
    } else {
        next(); // Proceed to the requested route
    }
});

export default router;