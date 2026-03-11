<template>
  <div class="admin-container">
    <h2>Admin Panel</h2>

    <div v-if="message">
      <p>{{ message }}</p>
    </div>

    <div v-else>
      <p>Loading admin panel...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "AdminPanel",

  data() {
    return {
      message: ""
    }
  },

  mounted() {
    this.loadAdminPanel()
  },

  methods: {
    async loadAdminPanel() {
      try {
        const token = localStorage.getItem("token")

        const response = await axios.get("http://127.0.0.1:5000/admin", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        this.message = response.data.message
      } catch (error) {
        console.error("Admin access error:", error)
      }
    }
  }
}
</script>

