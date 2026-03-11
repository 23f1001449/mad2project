<template>
  <div class="container">

    <h2>Create Placement Drive</h2>

    <div v-if="isApproved">
      <form @submit.prevent="createDrive">

        <div class="form-group">
          <label>Job Title</label>
          <input v-model="title" type="text" required>
        </div>

        <div class="form-group">
          <label>Job Description</label>
          <input v-model="description" type="text" required>
        </div>

        <div class="form-group">
          <label>Branch</label>
          <input v-model="branch" type="text" required>
        </div>

        <div class="form-group">
          <label>Minimum CGPA</label>
          <input v-model="cgpa" type="number" step="0.01" required>
        </div>

        <div class="form-group">
          <label>Deadline</label>
          <input v-model="deadline" type="datetime-local" required>
        </div>

        <button type="submit">Create Drive</button>

      </form>
    </div>

    <div v-else>
      <p class="info">{{ message }}</p>
    </div>

    <p v-if="message && isApproved" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "CreateDrive",

  data() {
    return {
      title: "",
      description: "",
      branch: "",
      cgpa: "",
      deadline: "",
      message: "",
      error: "",
      isApproved: false
    }
  },

  mounted() {
    this.checkApproval()
  },

  methods: {

    async checkApproval() {
      try {
        const token = localStorage.getItem("token")
        await axios.get("http://127.0.0.1:5000/company/applications", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        // If success, company is approved
        this.isApproved = true
      } catch (err) {
        if (err.response && err.response.status === 403) {
          // Pending approval
          this.isApproved = false
          this.message = "Your company registration is pending admin approval. You cannot create drives yet."
        } else {
          // Other error
          this.error = "Error checking approval status"
        }
      }
    },

    async createDrive() {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.post(
          "http://127.0.0.1:5000/drive/create",
          {
            job_title: this.title,
            job_description: this.description,
            branch: this.branch,
            cgpa_required: this.cgpa,
            deadline: this.deadline.replace("T", " ")
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message
        this.error = ""

        // redirect AFTER drive creation
        this.$router.push("/company/dashboard")

      } catch (err) {

        if (err.response) {
          this.error = err.response.data.error
        } else {
          this.error = "Server error"
        }

        this.message = ""

      }

    }

  }

}
</script>

