<template>
  <div class="container">

    <h2>Approve Companies</h2>

    <table v-if="companies.length">

      <thead>
        <tr>
          <th>ID</th>
          <th>Company Name</th>
          <th>HR Contact</th>
          <th>Website</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="company in companies" :key="company.id">

          <td>{{ company.id }}</td>
          <td>{{ company.company_name }}</td>
          <td>{{ company.hr_contact }}</td>
          <td>{{ company.website }}</td>

          <td>
            <button @click="approveCompany(company.id)">
              Approve
            </button>
          </td>

        </tr>

      </tbody>

    </table>

    <p v-if="!companies.length">No companies pending approval</p>

    <p v-if="message" class="success">{{ message }}</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "AdminApproveCompany",

  data() {
    return {
      companies: [],
      message: "",
      error: ""
    }
  },

  mounted() {
    this.fetchCompanies()
  },

  methods: {

    async fetchCompanies() {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.get(
          "http://127.0.0.1:5000/admin/companies",
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.companies = response.data

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"

      }

    },

    async approveCompany(id) {

      try {

        const token = localStorage.getItem("token")

        const response = await axios.put(
          `http://127.0.0.1:5000/admin/company/${id}/approve`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        )

        this.message = response.data.message
        this.error = ""

        // remove company from list
        this.companies = this.companies.filter(c => c.id !== id)

      } catch (err) {

        this.error = err.response?.data?.error || "Server error"

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
  padding:8px 12px;
  cursor:pointer;
}

.success{
  color:green;
}

.error{
  color:red;
}

</style>