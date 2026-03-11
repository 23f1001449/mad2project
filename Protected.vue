<template>
  <div class="protected-container">
    <h2>Protected Page</h2>

    <p v-if="message">{{ message }}</p>
    <p v-else>Loading protected content...</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Protected",

  data() {
    return {
      message: ""
    }
  },

  mounted() {
    this.loadProtected()
  },

  methods: {

    async loadProtected() {
      try {

        const token = localStorage.getItem("token")

        const response = await axios.get(
          "http://127.0.0.1:5000/protected",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message

      } catch (error) {
        console.error("Protected route error:", error)
      }

    }

  }
}
</script>

