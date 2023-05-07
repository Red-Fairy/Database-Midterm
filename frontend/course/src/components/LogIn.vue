<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="submitLogin">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
methods: {
  submitLogin() {
    // Hardcoded credentials for testing
    const users = [
      { username: 'admin', password: 'adminpassword', role: 'admin' },
      { username: 'user', password: 'userpassword', role: 'user' },
    ];

    const foundUser = users.find(
      (user) => user.username === this.username && user.password === this.password
    );

    if (foundUser) {
      // Store the access token and user role in localStorage
      localStorage.setItem('accessToken', 'hardcodedaccesstoken');
      localStorage.setItem('userRole', foundUser.role);

      // Navigate to the appropriate page based on the user's role
      if (foundUser.role === 'admin') {
        this.$router.push('/admin');
      } else if (foundUser.role === 'user') {
        this.$router.push('/user');
      } else {
        this.error = 'Invalid user role';
      }
    } else {
      this.error = 'Invalid username or password';
    }
  },
},
};
</script>
