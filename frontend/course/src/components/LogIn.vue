<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="handleSubmit">
            <div>
                <label for="username">Username:</label>
                <input id="username" v-model="username" type="text" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input id="password" v-model="password" type="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>
  
<script>
import api from '@/api';

export default {
    data() {
        return {
            username: '',
            password: '',
        };
    },
    methods: {
        async handleSubmit() {
            try {
                const response = await api.login(this.username, this.password);
                localStorage.setItem('accessToken', response.data.accessToken);
                localStorage.setItem('userRole', response.data.userRole);
                this.$router.push({ name: 'dashboard' }); // Navigate to the dashboard or another appropriate route
                // Save access token and user role, then navigate to the appropriate page
            } catch (error) {
                // Handle login error
            }
        },
    },
};
</script>
  