<template>
  <div class="applications-container">
    <h2>My Applications</h2>

    <table v-if="applications.length > 0">
      <thead>
        <tr>
          <th>Application ID</th>
          <th>Job Title</th>
          <th>Company</th>
          <th>Status</th>
          <th>Deadline</th>
          <th>Interview Date</th>
          <th>Download</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="app in applications" :key="app.application_id">
          <td>{{ app.application_id }}</td>
          <td>{{ app.job_title }}</td>
          <td>{{ app.company }}</td>
          <td>{{ app.status }}</td>
          <td>{{ app.deadline }}</td>
          <td>{{ app.interview_date || "Not Scheduled" }}</td>
          <td>
            <button v-if="app.interview_date || ['Shortlisted','Selected','Rejected'].includes(app.status)" @click="downloadReport(app.id)">Download</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Loading applications...</p>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "MyApplications",

  data() {
    return {
      applications: []
    }
  },

  mounted() {
    this.fetchApplications()
  },

  methods: {

    async fetchApplications() {
      try {

        const token = localStorage.getItem("token")

        const response = await axios.get(
          "http://127.0.0.1:5000/myapplications",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.applications = response.data

      } catch (error) {

        if (error.response && error.response.data.error) {
          console.error(error.response.data.error)
        } else {
          console.error("Failed to load applications")
        }

      }
    },
    async exportApplications() {

  try {

    const token = localStorage.getItem("token")

    const response = await axios.post(
      "http://127.0.0.1:5000/export",
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    this.message = response.data.message

  } catch (error) {

    this.message = "Export failed"

  }

}

  }
}
</script>

