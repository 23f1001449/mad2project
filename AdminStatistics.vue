<template>
  <div class="container">

    <h2>Placement Statistics</h2>

    <div class="stats-cards">

      <div class="card">
        Total Students
        <span>{{ stats.total_students }}</span>
      </div>

      <div class="card">
        Total Companies
        <span>{{ stats.total_companies }}</span>
      </div>

      <div class="card">
        Total Drives
        <span>{{ stats.total_drives }}</span>
      </div>

      <div class="card">
        Total Applications
        <span>{{ stats.total_applications }}</span>
      </div>

      <div class="card">
        Selected Students
        <span>{{ stats.selected_students }}</span>
      </div>

    </div>

    <h3>Applications per Company</h3>

    <table v-if="stats.applications_per_company && stats.applications_per_company.length">

      <thead>
        <tr>
          <th>Company</th>
          <th>Applications</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="item in stats.applications_per_company"
          :key="item.company"
        >
          <td>{{ item.company }}</td>
          <td>{{ item.applications }}</td>
        </tr>

      </tbody>

    </table>

    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "AdminStatistics",

  data() {
    return {
      stats: {
        total_students: 0,
        total_companies: 0,
        total_drives: 0,
        total_applications: 0,
        selected_students: 0,
        applications_per_company: []
      },
      error: ""
    }
  },

  mounted() {
    this.fetchStatistics()
  },

  methods: {

    async fetchStatistics() {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.get(
          "http://127.0.0.1:5000/reports/statistics",
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.stats = response.data

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"

      }

    }

  }

}
</script>

