<template>
  <div class="container">
    <h2>Register Company</h2>

    <div v-if="!isRegistered">
      <form @submit.prevent="registerCompany">

        <div class="form-group">
          <label>Company Name</label>
          <input v-model="company_name" type="text" required />
        </div>

        <div class="form-group">
          <label>HR Contact</label>
          <input v-model="hr_contact" type="text" required />
        </div>

        <div class="form-group">
          <label>Website</label>
          <input v-model="website" type="text" required />
        </div>

        <button type="submit">Register Company</button>

      </form>
    </div>

    <div v-else-if="isRegistered && !isApproved">
      <p class="info">{{ message }}</p>
    </div>

    <p v-if="message && !isRegistered" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyRegister",

  data() {
    return {
      company_name: "",
      hr_contact: "",
      website: "",
      message: "",
      error: "",
      isRegistered: false,
      isApproved: false
    }
  },

  mounted() {
    this.checkRegistration()
  },

  methods: {

    async checkRegistration() {
      try {
        const token = localStorage.getItem("token")
        await axios.get("http://127.0.0.1:5000/company/applications", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        // If success, company is registered and approved, redirect to applications
        this.$router.push("/company/applications/updated")
      } catch (err) {
        if (err.response && err.response.status === 403) {
          // Pending approval
          this.isRegistered = true
          this.message = "Your company registration is pending admin approval."
        } else if (err.response && err.response.status === 404) {
          // Not registered
          this.isRegistered = false
        } else {
          // Other error
          this.error = "Error checking registration status"
        }
      }
    },

    async registerCompany() {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.post(
          "http://127.0.0.1:5000/company/register",
          {
            company_name: this.company_name,
            hr_contact: this.hr_contact,
            website: this.website
          },
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message
        this.error = ""
        this.isRegistered = true
        this.message = "Company registration submitted for approval. Please wait for admin approval."

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

