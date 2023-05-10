<template>
    <!-- Add this inside the template section -->
    <template v-if="isAdmin">
        <table>
            <thead>
                <tr>
                    <th>User ID</th>
                    <th>Role</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(user, index) in courseUsers" :key="index">
                    <td>{{ user.userID }}</td>
                    <td>{{ user.teacher ? 'Teacher' : 'Student' }}</td>
                    <td>
                        <!-- Add actions for editing and deleting users here -->
                    </td>
                </tr>
            </tbody>
        </table>
    </template>

    <div class="course-dashboard">
        <h1>{{ courseID }} - Course Dashboard</h1>
        <h2>Teachers</h2>
        <ul>
            <li v-for="teacher in teachers" :key="teacher.userID">{{ teacher.username }}</li>
        </ul>
        <h2>Students</h2>
        <ul>
            <li v-for="student in students" :key="student.userID">{{ student.username }}</li>
        </ul>
    </div>
</template>
  
<script>
// import api from '@/api';

export default {
    data() {
        return {
            courseUsers: [],
            // ... other data properties
        };
    },
    async created() {
        this.courseUsers = await this.$api.getCourseUsers(this.courseID);
    },
    methods: {
        async updateCourseUser(method, userID, teacher) {
            try {
                await this.$api.updateUserCourseRelation(method, this.courseID, userID, teacher);
                // Refresh courseUsers after successful update
                this.courseUsers = await this.$api.getCourseUsers(this.courseID);
            } catch (error) {
                console.error('Error updating course user:', error);
            }
        },
        // ... other methods
    },
    computed: {
        isAdmin() {
            // Check if the user has admin permissions by examining the value stored in localStorage
            return localStorage.getItem('permission') === 'admin';
        },
    },

};

</script>
  