<template>
    <div class="register">
        <h1>Register</h1>
        <form @submit.prevent="register">
            <div class="form-field">
                <label for="userid">User ID:</label>
                <input type="text" id="userid" v-model="userid" />
            </div>
            <div class="form-field">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" />
            </div>
            <div class="form-field">
                <button type="submit" class="form-button">Register</button>
            </div>
            <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>
        </form>
        <div class="form-field">
            <button @click.prevent="goToLogin" class="form-button secondary-button">Back to Login</button>
        </div>
    </div>
</template>
  
<script>
import api from "@/api";

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
                const response = await api.register(this.userid, this.password);

                if (response.status === "200") {
                    this.errorMsg = "注册成功";
                } else {
                    this.errorMsg = response.msg;
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
    padding: 1em;
    background-color: #F5F5F5;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

form {
    display: flex;
    flex-direction: column;
}

.form-field {
    margin-bottom: 1em;
}

.form-field label {
    font-weight: bold;
    margin-bottom: 0.5em;
    display: block;
}

.form-field input {
    padding: 0.5em;
    border: 1px solid #DDD;
    border-radius: 4px;
}

.form-button {
    padding: 0.5em 1em;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.form-button:hover {
    background-color: #0056b3;
}

.secondary-button {
    background-color: #6c757d;
}

.secondary-button:hover {
    background-color: #5a6268;
}

.error-message {
    color: #dc3545;
    font-weight: bold;
}

button {
    margin-top: 1em;
}
</style>