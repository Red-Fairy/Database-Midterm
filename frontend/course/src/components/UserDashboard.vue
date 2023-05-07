<template>
  <div>
    <h1>User Dashboard</h1>
    <p>Welcome, user! This is your dashboard.</p>
    <div>
      <h2>Search Users</h2>
      <label for="search">Search:</label>
      <input type="text" id="search" v-model="searchQuery" @input="searchUsers" />
    </div>
    <data-table ref="dataTable" :isAdmin="false"></data-table>
  </div>
</template>

<script>
import DataTable from './DataTable.vue';
import axios from 'axios';

export default {
  name: 'UserDashboard',
  components: {
    DataTable,
  },
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    async searchUsers() {
      try {
        const response = await axios.get("http://localhost:5000/api/users/search", {
          params: { query: this.searchQuery },
        });
        this.$refs.dataTable.updateData(response.data);
      } catch (error) {
        console.error("Error searching users:", error);
      }
    },
  },
};
</script>