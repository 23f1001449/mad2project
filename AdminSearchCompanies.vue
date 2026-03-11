<template>
  <div class="container">

    <h2>Search Companies</h2>

    <div class="search-bar">
      <input v-model="query" type="text" placeholder="Enter company name" />
      <button @click="searchCompanies">Search</button>
    </div>

    <table v-if="companies.length">

      <thead>
        <tr>
          <th>Company ID</th>
          <th>Name</th>
          <th>Website</th>
          <th>HR Contact</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="company in companies" :key="company.company_id">
          <td>{{ company.company_id }}</td>
          <td>{{ company.name }}</td>
          <td>{{ company.website }}</td>
          <td>{{ company.hr_contact }}</td>
        </tr>
      </tbody>

    </table>

    <p v-if="!companies.length && searched">No companies found</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "AdminSearchCompanies",

  data() {
    return {
      query: "",
      companies: [],
      error: "",
      searched: false
    }
  },

  methods: {

    async searchCompanies() {

      if (!this.query.trim()) {
        this.error = "Please enter a search query"
        return
      }

      try {
        const token = localStorage.getItem("token")

        const response = await axios.get(
          `http://127.0.0.1:5000/search/companies?q=${encodeURIComponent(this.query)}`,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.companies = response.data
        this.error = ""
        this.searched = true

      } catch (err) {
        this.error = err.response?.data?.error || "Server error"
        this.companies = []
      }

    }

  }

}
</script>

