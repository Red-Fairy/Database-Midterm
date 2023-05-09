<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="userid">User ID:</label>
        <input type="text" id="userid" v-model="userid" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" />
      </div>
      <div>
        <button type="submit">Login</button>
      </div>
      <div>
        <button @click.prevent="goToRegister">Register</button>
      </div>
      <div v-if="errorMsg">{{ errorMsg }}</div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userid: "",
      password: "",
      errorMsg: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("/api/user/login", {
          userid: this.userid,
          password: this.password,
        });

        if (response.data.code === 200) {
          this.errorMsg = "";
          localStorage.setItem("token", response.data.token);
          localStorage.setItem("permission", response.data.permission);

          // Redirect to the appropriate dashboard
          if (response.data.permission === 'admin') {
            this.$router.push("/admin");
          } else if (response.data.permission === 'teacher') {
            this.$router.push("/teacher");
          } else {
            this.$router.push("/student");
          }
        } else {
          this.errorMsg = response.data.msg;
        }
      } catch (error) {
        this.errorMsg = "An error occurred. Please try again.";
      }
    },
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>