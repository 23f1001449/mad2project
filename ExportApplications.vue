<template>
  <div class="container">
    <div class="card" style="text-align:center;">
      <h2>Export My Applications</h2>
      <p>Click the button below to export your applications to CSV.</p>

      <button class="btn-primary" @click="exportApplications" style="width: 100%; margin-top: 15px;">
        Export CSV
      </button>

      <p v-if="message" :class="message.includes('success') ? 'success' : 'error'" style="margin-top:10px;">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ExportApplications",
  data() {
    return { message: "" };
  },
  methods: {
    async exportApplications() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(
          "http://127.0.0.1:5000/export",
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.message = response.data.message;
      } catch (error) {
        this.message =
          error.response?.data?.error || "Export failed";
      }
    },
  },
};
</script>