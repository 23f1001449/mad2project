<template>
  <div class="drives-container">
    <h2>Available Placement Drives</h2>

    <table v-if="drives.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Job Title</th>
          <th>Branch</th>
          <th>CGPA Required</th>
          <th>Deadline</th>
          <th>Company</th>
          <th>Website</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="drive in drives" :key="drive.id">
          <td>{{ drive.id }}</td>
          <td>{{ drive.title }}</td>
          <td>{{ drive.branch }}</td>
          <td>{{ drive.cgpa }}</td>
          <td>{{ drive.deadline }}</td>
          <td>{{ drive.company_name }}</td>
          <td>
            <a :href="drive.company_website" target="_blank">
              Visit
            </a>
          </td>
          <td>
            <button :disabled="drive.applied" @click="applyDrive(drive.id)">Apply</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="drives.length === 0">No drives available</p>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Drives",

  data() {
    return {
      drives: []
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
          "http://127.0.0.1:5000/drives",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.drives = response.data

      } catch (error) {
        console.error("Error fetching drives:", error)
      }
    },
    



    async applyDrive(id) {

  try {

    const token = localStorage.getItem("token")

    await axios.post(
      `http://127.0.0.1:5000/apply/${id}`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    alert("Application submitted successfully")

    this.$router.push("/myapplications")

  } catch (error) {

    alert("Could not apply for this drive")

  }

}
  }
}
</script>

