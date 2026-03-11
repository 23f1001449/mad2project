<template>
  <div class="applications-container">
    <h2>All Users</h2>

    <table v-if="users.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>Loading users...</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "AllUsers",

  data() {
    return {
      users: []
    }
  },

  mounted() {
    this.fetchUsers()
  },

  methods: {
    async fetchUsers() {
      try {
        const token = localStorage.getItem("token")

        const response = await axios.get("http://127.0.0.1:5000/allusers", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        this.users = response.data
      } catch (error) {
        console.error("Error fetching users:", error)
      }
    }
  }
}
</script>

