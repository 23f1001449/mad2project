<template>
  <div class="update-container">
    <h2>Update Profile</h2>

    <form @submit.prevent="updateProfile">

      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" />
      </div>

      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" />
      </div>

      <button type="submit">Update Profile</button>
    </form>

    <p v-if="message">{{ message }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "UpdateProfile",

  data() {
    return {
      username: "",
      email: "",
      password: "",
      message: ""
    }
  },

  methods: {
    async updateProfile() {
      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(
          "http://127.0.0.1:5000/updateprofile",
          {
            username: this.username,
            email: this.email,
            password: this.password
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message

      } catch (error) {
        console.error("Update error:", error)
      }
    }
  }
}
</script>

