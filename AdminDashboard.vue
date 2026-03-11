<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <div v-if="user">
      <h2>Welcome, {{ user.username }}!</h2>
      <div class="dashboard-grid">
        <div class="dashboard-card" @click="$router.push('/admin/approve-company')">
          <h3>Approve Companies</h3>
          <p>Review and approve company registrations.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/admin/approve-drives')">
          <h3>Approve Drives</h3>
          <p>Review and approve placement drives.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/admin/search-students')">
          <h3>Search Students</h3>
          <p>Search and manage student accounts.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/admin/search-companies')">
          <h3>Search Companies</h3>
          <p>Search and manage company accounts.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/admin/statistics')">
          <h3>View Statistics</h3>
          <p>View system statistics and reports.</p>
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
  name: "AdminDashboard",
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
.admin-dashboard {
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