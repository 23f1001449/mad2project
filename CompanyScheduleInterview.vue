<template>
  <div class="container">

    <h2>Schedule Interview</h2>

    <form @submit.prevent="scheduleInterview">

      <div class="form-group">
        <label>Application ID</label>
        <input v-model="application_id" type="number" required />
      </div>

      <div class="form-group">
        <label>Interview Date & Time</label>
        <input v-model="interview_date" type="datetime-local" required />
      </div>

      <button type="submit">Schedule Interview</button>

    </form>

    <p v-if="message" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "CompanyScheduleInterview",

  data() {
    return {
      application_id: "",
      interview_date: "",
      message: "",
      error: ""
    }
  },

  methods: {

    async scheduleInterview() {

      try {

        const token = localStorage.getItem("token")

        // convert datetime-local format
        const formattedDate = this.interview_date.replace("T", " ")

        const response = await axios.put(
          `http://127.0.0.1:5000/application/${this.application_id}/scheduleinterview`,
          {
            interview_date: formattedDate
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message
        this.error = ""

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"
        this.message = ""

      }

    }

  }

}
</script>

