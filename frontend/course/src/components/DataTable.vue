<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th v-if="isAdmin">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in data" :key="row.ID">
          <td>{{ row.ID }}</td>
          <td v-if="!isEditing(row)">
            {{ row.Name }}
          </td>
          <td v-else>
            <input type="text" v-model="row.Name" />
          </td>
          <td>{{ row.Email }}</td>
          <td v-if="isAdmin">
            <button @click="deleteUser(row.ID)">Delete</button>
            <button v-if="!isEditing(row)" @click="startEditUser(row)">Edit</button>
            <div v-else>
              <button @click="updateUser">Save</button>
              <button @click="cancelUpdate">Cancel</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    isAdmin: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      data: [],
      editingUser: null,
      originalUserData: null,
    };
  },
  methods: {
    fetchData() {
      axios
        .get("http://localhost:5000/api/data")
        .then((response) => {
          this.data = response.data;
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    updateData(newData) {
      this.data = newData;
    },
    async deleteUser(id) {
      try {
        await axios.delete(`http://localhost:5000/api/users/${id}`);
        this.fetchData();
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    },
    startEditUser(user) {
      this.originalUserData = { ...user };
      this.editingUser = user;
    },

    async updateUser() {
      try {
        await axios.put(`http://localhost:5000/api/users/${this.selectedUser.ID}`, {
          Name: this.selectedUser.Name,
          Email: this.selectedUser.Email,
        });
        this.$refs.dataTable.fetchData(); // Refresh the data table
      } catch (error) {
        console.error("Error updating user:", error);
      }
    },
    cancelUpdate() {
      Object.assign(this.editingUser, this.originalUserData);
      this.editingUser = null;
    },
    isEditing(user) {
      return this.editingUser && this.editingUser.ID === user.ID;
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  font-weight: bold;
}
</style>
