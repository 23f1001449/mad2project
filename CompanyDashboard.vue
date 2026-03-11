<template>
  <div class="company-dashboard">
    <h1>Company Dashboard</h1>
    <div v-if="user">
      <h2>Welcome, {{ user.username }}!</h2>
      <div class="dashboard-grid">
        <div class="dashboard-card" @click="$router.push('/company/register')">
          <h3>Register Company</h3>
          <p>Register your company details.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/drive/create')">
          <h3>Create Drive</h3>
          <p>Create a new placement drive.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/company/applications/updated')">
          <h3>View Applications</h3>
          <p>Review applications for your drives.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/schedule-interview')">
          <h3>Schedule Interviews</h3>
          <p>Schedule interviews for candidates.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/logout')">
          <h3>Logout</h3>
          <p>Sign out of your account.</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CompanyDashboard",
  data() {
    return {
      user: null
    };
  },
  mounted() {
    this.getProfile();
  },
  methods: {
    async getProfile() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/profile", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
        this.$router.push("/");
      }
    }
  }
};
</script>

<style scoped>
.company-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.dashboard-card {
  background: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: background 0.3s;
}

.dashboard-card:hover {
  background: #e9e9e9;
}

.dashboard-card h3 {
  margin-top: 0;
  color: #333;
}

.dashboard-card p {
  color: #666;
}
</style>