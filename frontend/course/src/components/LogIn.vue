<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="logIn">
      <div>
        <label for="userid">User ID:</label>
        <input type="text" id="userid" v-model="userid" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <div class="button-container">
        <button type="submit">Login</button>
        <button type="button" @click.prevent="goToRegister">Register</button>
      </div>
      <div v-if="errorMsg">{{ errorMsg }}</div>
    </form>
  </div>
</template>

<script>
// import axios from "axios";
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
          // 登录成功，保存 token 和 permission 到 localStorage
          localStorage.setItem('token', response.token);
          localStorage.setItem('permission', response.permission);
          localStorage.setItem('userID', this.userid); // 将用户名存储到localStorage

          // 根据权限重定向到相应的页面
          if (response.permission) {
            // 如果用户是 admin，重定向到 AdminDashboard
            this.$router.push({ name: 'AdminDashboard' });
          } else {
            // 如果用户是 user，重定向到 UserDashboard
            this.$router.push({ name: 'UserDashboard' });
          }
        } else {
          // 登录失败，显示错误信息
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
.login {
  width: 400px;
  margin: 0 auto;
}

.button-container {
  margin-top: 10px;
  text-align: center;
}

.button-container button {
  display: inline-block;
  margin-right: 10px;
}
</style>