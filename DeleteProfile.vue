<template>
  <div class="delete-container">
    <div class="card">
      <h2>Delete Profile</h2>

      <p class="text-center">This action cannot be undone.</p>

      <button @click="deleteProfile" style="background-color: #d32f2f; width: 100%; margin-top: 20px;">Delete My Account</button>

      <p v-if="message" class="info" style="margin-top: 15px;">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "DeleteProfile",

  data() {
    return {
      message: ""
    }
  },

  methods: {
    async deleteProfile() {
      try {

        const token = localStorage.getItem("token")

        const response = await axios.delete(
          "http://127.0.0.1:5000/deleteprofile",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message

        // remove token
        localStorage.removeItem("token")

        // redirect to login
        this.$router.push("/login")

      } catch (error) {
        console.error("Delete profile error:", error)
      }
    }
  }
}
</script>

