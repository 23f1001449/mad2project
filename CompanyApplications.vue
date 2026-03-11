<template>
  <div class="container">

    <h2>Applications for Your Drives</h2>

    <table v-if="applications.length">

      <thead>
        <tr>
          <th>Application ID</th>
          <th>Student Name</th>
          <th>Job Title</th>
          <th>Status</th>
          <th>Update Status</th>
          <th>Interview</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="app in applications" :key="app.application_id">

          <td>{{ app.application_id }}</td>
          <td>{{ app.student_name }}</td>
          <td>{{ app.job_title }}</td>

          <td :class="'status-' + statusColor(app.status).toLowerCase()">
            {{ app.status }}
          </td>

          <td>

            <select v-model="app.newStatus">
              <option disabled value="">Select</option>
              <option>Shortlisted</option>
              <option>Rejected</option>
              <option>Selected</option>
            </select>

            <button @click="updateStatus(app)">Update</button>

          </td>
          <td>

            <input
              type="datetime-local"
              v-model="app.interview_date"
              :disabled="app.status !== 'Shortlisted'"
            />

            <button @click="scheduleInterview(app)">
              Schedule
            </button>

          </td>
        </tr>
      </tbody>

    </table>

    <p v-if="!applications.length">No applications found</p>

    <p v-if="message" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "CompanyApplications",

  data() {
    return {
      applications: [],
      message: "",
      error: ""
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
          "http://127.0.0.1:5000/company/applications",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.applications = response.data.map(app => ({
          ...app,
          newStatus: "",
          interview_date: ""
        }))

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"

      }

    },

    async updateStatus(app) {

      if (!app.newStatus) {
        this.error = "Please select a status"
        return
      }

      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(
          `http://127.0.0.1:5000/application/${app.application_id}/status`,
          { status: app.newStatus },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message
        this.error = ""

        app.status = app.newStatus
        app.newStatus = ""

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"
        this.message = ""

      }

    },

    statusColor(status) {

      if (status === "Selected") return "selected"
      if (status === "Rejected") return "rejected"
      if (status === "Shortlisted") return "shortlisted"

      return "applied"
    },
    async scheduleInterview(app) {

    if (!app.interview_date) {
    this.error = "Please select interview date"
    return
  }

  try {

    const token = localStorage.getItem("token")

    const formattedDate = app.interview_date.replace("T"," ")

    const response = await axios.put(
      `http://127.0.0.1:5000/application/${app.application_id}/scheduleinterview`,
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


<style scoped>

.container{
  width:900px;
  margin:auto;
}

table{
  width:100%;
  border-collapse:collapse;
  margin-top:20px;
}

th, td{
  border:1px solid #ccc;
  padding:10px;
  text-align:center;
}

th{
  background:#f5f5f5;
  color:#333;
}

button{
  margin-left:5px;
  padding:5px 10px;
  cursor:pointer;
}

select{
  padding:5px;
}

.status-selected {
  color: green;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  vertical-align: middle;
}

.status-rejected {
  color: red;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  vertical-align: middle;
}

.status-shortlisted {
  color: orange;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  vertical-align: middle;
}

.status-applied {
  color: #333;
  font-weight: normal;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
  vertical-align: middle;
}

</style>