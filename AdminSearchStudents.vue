<template>
  <div class="container">

    <h2>Search Students</h2>

    <div class="search-bar">
      <input v-model="query" type="text" placeholder="Enter name, branch, skill, or email" />
      <button @click="searchStudents">Search</button>
    </div>

    <table v-if="students.length">

      <thead>
        <tr>
          <th>Student ID</th>
          <th>Full Name</th>
          <th>Email</th>
          <th>Branch</th>
          <th>CGPA</th>
          <th>Skills</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="student in students" :key="student.student_id">
          <td>{{ student.student_id }}</td>
          <td>{{ student.full_name }}</td>
          <td>{{ student.email }}</td>
          <td>{{ student.branch }}</td>
          <td>{{ student.cgpa }}</td>
          <td>{{ student.skills }}</td>
        </tr>
      </tbody>

    </table>

    <p v-if="!students.length && searched">No students found</p>
    <p v-if="error" class="error">{{ error }}</p>

  </div>
</template>

<script>
import axios from "axios"

export default {

  name: "AdminSearchStudents",

  data() {
    return {
      query: "",
      students: [],
      error: "",
      searched: false
    }
  },

  methods: {

    async searchStudents() {

      if (!this.query.trim()) {
        this.error = "Please enter a search query"
        return
      }

      try {
        const token = localStorage.getItem("token")

        const response = await axios.get(
          `http://127.0.0.1:5000/search/students?q=${encodeURIComponent(this.query)}`,
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        )

        this.students = response.data
        this.error = ""
        this.searched = true

      } catch (err) {
        this.error = err.response?.data?.error || "Server error"
        this.students = []
      }

    }

  }

}
</script>

