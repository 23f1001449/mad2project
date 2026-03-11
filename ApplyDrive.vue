<template>
  <div class="container">
    <h2>Apply for Drive</h2>
    <p>Drive ID: {{ $route.params.id }}</p>
    <button @click="apply">Apply</button>
  </div>
</template>

<script>
import axios from "axios"
export default {
  methods: {
    async apply() {
      const token = localStorage.getItem("token")
      const id = this.$route.params.id
      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/apply/${id}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )
        alert(response.data.message)
        this.$router.push('/drives')
      } catch (error) {
        if (error.response && error.response.data.error) {
          alert(error.response.data.error)
        } else {
          alert("An error occurred")
        }
      }
    }
  }
}
</script>