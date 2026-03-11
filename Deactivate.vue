<template>
  <div class="container">
    <h2>Deactivate User</h2>

    <form @submit.prevent="deactivateUser">
      <div class="form-group">
        <label>User ID:</label>
        <input v-model="userId" type="number" required />
      </div>

      <button type="submit">Deactivate User</button>
    </form>

    <p v-if="message" class="info">{{ message }}</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "DeactivateUser",

  data() {
    return {
      userId: "",
      message: ""
    }
  },

  methods: {

    async deactivateUser() {
      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(
          `http://127.0.0.1:5000/user/${this.userId}/deactivate`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message

      } catch (error) {
        console.error("Deactivate error:", error)
      }
    }

  }
}
</script>

