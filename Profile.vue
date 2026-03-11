<template>
  <div class="profile-container">
    <h2>User Profile</h2>

    <div v-if="user">
      <p><strong>ID:</strong> {{ user.id }}</p>
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Role:</strong> {{ user.role }}</p>
      <button @click="$router.push('/fulluserprofile')">Create Student Profile</button>
    </div>

    <div v-else>
      <p>Loading profile...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Profile",

  data() {
    return {
      user: null
    }
  },

  mounted() {
    this.getProfile()
  },

  methods: {
    async getProfile() {
      try {
        const token = localStorage.getItem("token")

        const response = await axios.get("http://127.0.0.1:5000/profile", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        this.user = response.data
      } catch (error) {
        console.error("Error fetching profile:", error)
      }
    }
  }
}
</script>

