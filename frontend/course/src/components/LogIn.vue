<template>
  <h1 class="title">校园课程管理系统</h1>
  <div class="login">
    <h2>请登录：</h2>
    <form @submit.prevent="logIn">
      <div class="form-group">
        <label for="userid">User ID:</label>
        <input type="text" id="userid" v-model="userid" class="input-field" />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" class="input-field" />
      </div>
      <div class="button-container">
        <button type="submit" class="button-primary">Login</button>
        <button type="button" @click.prevent="goToRegister" class="button-secondary">Register</button>
      </div>
      <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
    </form>
  </div>
</template>

<script>
import api from '@/api';

export default {
  data() {
    return {
      userid: "",
      password: "",
      errorMsg: "",
    };
  },

  methods: {
    async logIn() {
      try {
        const response = await api.login(this.userid, this.password);
        if (response.code === 200) {
          localStorage.setItem('token', response.token);
          localStorage.setItem('permission', response.permission);
          localStorage.setItem('userID', this.userid);

          if (response.permission) {
            this.$router.push({ name: 'AdminDashboard' });
          } else {
            this.$router.push({ name: 'UserDashboard' });
          }
        } else {
          this.errorMsg = response.msg;
        }
      } catch (error) {
        console.error('Login error:', error);
        this.errorMsg = '登录失败，请稍后重试。';
      }
    },
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
.title {
  text-align: center;
  margin-bottom: 20px;
}

.login {
  width: 400px;
  margin: 0 auto;
  text-align: center;
}

.form-group {
  margin-bottom: 10px;
}

.label {
  display: block;
  font-weight: bold;
}

.input-field {
  padding: 5px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
}

.button-container {
  margin-top: 10px;
}

.button-primary {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button-secondary {
  padding: 10px 20px;
  background-color: #ccc;
  color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
