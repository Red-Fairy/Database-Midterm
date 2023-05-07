<!-- AdminDashboard.vue -->
import DataTable from './DataTable.vue';

<template>
    <div>
        <h2>Admin Dashboard</h2>
        <p>Welcome, admin! This is your dashboard.</p>
        <div>
            <h2>Add User</h2>
            <form @submit.prevent="addUser">
                <label for="name">Name:</label>
                <input type="text" id="name" v-model="newUser.Name" />
                <br />
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="newUser.Email" />
                <br />
                <button type="submit">Add User</button>
            </form>
        </div>
        <data-table ref="dataTable" :isAdmin="true"></data-table>
        <!-- Add your admin dashboard content here -->
    </div>
</template>

<script>
import DataTable from './DataTable.vue';
import axios from 'axios';
export default {
    name: 'AdminDashboard',
    components: {
        DataTable,
    },
    data() {
        return {
            newUser: {
                Name: "",
                Email: "",
            },
        };
    },
    methods: {
        async addUser() {
            try {
                await axios.post("http://localhost:5000/api/users", this.newUser);
                this.newUser.Name = "";
                this.newUser.Email = "";
                this.$refs.dataTable.fetchData(); // Refresh the data table
            } catch (error) {
                console.error("Error adding user:", error);
            }
        },
    },
};
</script>

<style scoped>
/* Add your AdminDashboard-specific styles here */
</style>
