<template>
    <div class="register">
        <h1>Register</h1>
        <form @submit.prevent="register">
            <div>
                <label for="userid">User ID:</label>
                <input type="text" id="userid" v-model="userid" />
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" />
            </div>
            <div>
                <button type="submit">Register</button>
            </div>
            <div v-if="errorMsg">{{ errorMsg }}</div>
        </form>
        <div>
            <button @click.prevent="goToLogin">Back to Login</button>
        </div>
    </div>
</template>
  
<script>
import axios from "axios";

export default {
    data() {
        return {
            userid: "",
            password: "",
            role: "teacher",
            errorMsg: "",
        };
    },
    methods: {
        async register() {
            try {
                const response = await axios.post("/api/user/register", {
                    username: this.userid, // 将userid更改为username，以匹配后端API
                    password: this.password,
                });

                if (response.data.status === "200") {
                    this.errorMsg = "";
                    this.$router.push("/login");
                } else {
                    this.errorMsg = response.data.msg;
                }
            } catch (error) {
                this.errorMsg = "An error occurred. Please try again.";
            }
        },
        goToLogin() {
            this.$router.push("/login");
        },
    },
};
</script>
  
<style scoped>
.register {
    max-width: 300px;
    margin: 0 auto;
}

form {
    display: flex;
    flex-direction: column;
}

button {
    margin-top: 1em;
}
</style>
  