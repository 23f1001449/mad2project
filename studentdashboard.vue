<template>
  <div class="student-dashboard">
    <h1>Student Dashboard</h1>
    <div v-if="user">
      <h2>Welcome, {{ user.username }}!</h2>
      <div class="dashboard-grid">
        <div class="dashboard-card" @click="$router.push('/profile')">
          <h3>View Profile</h3>
          <p>Check and manage your basic profile information.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/fulluserprofile')">
          <h3>Student Profile</h3>
          <p>Update your detailed student profile.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/drives')">
          <h3>Browse Drives</h3>
          <p>View available placement drives and apply.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/myapplications')">
          <h3>My Applications</h3>
          <p>Check the status of your job applications.</p>
        </div>
        <div class="dashboard-card" @click="$router.push('/updateprofile')">
          <h3>Update Profile</h3>
          <p>Edit your account information.</p>
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
  name: "StudentDashboard",
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
.student-dashboard {
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