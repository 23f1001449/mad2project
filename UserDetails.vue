<template>
  <div class="container">
    <h2>User Details</h2>

    <div class="search-bar">
      <input v-model="userId" type="number" placeholder="Enter User ID" />
      <button @click="fetchUser">Get User</button>
    </div>

    <div v-if="user" class="card">
      <h3>User Info</h3>
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Role:</strong> {{ user.role }}</p>

      <button @click="deleteUser" style="background-color: #d32f2f; margin-top: 15px;">Delete User</button>
    </div>

    <p v-if="message" class="info">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "UserDetails",

  data() {
    return {
      userId: "",
      user: null,
      message: ""
    }
  },

  methods: {

    async fetchUser() {
      try {
        const token = localStorage.getItem("token")

        const response = await axios.get(
          `http://127.0.0.1:5000/user/${this.userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.user = response.data

      } catch (error) {
        console.error("Fetch error:", error)
      }
    },

    async deleteUser() {
      try {

        const token = localStorage.getItem("token")

        const response = await axios.delete(
          `http://127.0.0.1:5000/user/${this.userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message
        this.user = null

      } catch (error) {
        console.error("Delete error:", error)
      }
    }

  }
}
</script>

