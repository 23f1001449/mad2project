<template>
  <div class="container">

    <h2>Approve Placement Drives</h2>

    <table v-if="drives.length">

      <thead>
        <tr>
          <th>Drive ID</th>
          <th>Company</th>
          <th>Job Title</th>
          <th>Branch</th>
          <th>CGPA Required</th>
          <th>Deadline</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="drive in drives" :key="drive.id">

          <td>{{ drive.id }}</td>
          <td>{{ drive.company_name }}</td>
          <td>{{ drive.job_title }}</td>
          <td>{{ drive.branch }}</td>
          <td>{{ drive.cgpa_required }}</td>
          <td>{{ drive.deadline }}</td>

          <td>
            <button @click="approveDrive(drive.id)">
              Approve
            </button>
          </td>

        </tr>

      </tbody>

    </table>

    <p v-else>No placement drives pending approval</p>

    <p v-if="message" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "AdminApproveDrives",

  data() {
    return {
      drives: [],
      message: "",
      error: ""
    }
  },

  mounted() {
    this.fetchDrives()
  },

  methods: {

    async fetchDrives() {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/drives",
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.drives = response.data

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"

      }

    },

    async approveDrive(id) {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(
          `http://127.0.0.1:5000/admin/drive/${id}/approve`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.message = response.data.message
        this.error = ""

        // remove drive from list
        this.drives = this.drives.filter(d => d.id !== id)

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"
        this.message = ""

      }

    }

  }

}
</script>

