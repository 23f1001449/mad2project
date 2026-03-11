<template>
    <div class="register-container">
        <h2>Register</h2>
        <form @submit.prevent="register">
          <div class="form-group">
            <label>Username</label>
            <input v-model="username" type="text" placeholder="Username" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="email" type="email" placeholder="Email" required />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input v-model="password" type="password" placeholder="Password" required />
          </div>
          <div class="form-group">
            <label>Role</label>
            <select v-model="role" required>
                <option value="">Select Role</option>
                <option value="student">Student</option>
                <option value="company">Company</option>
            </select>
          </div>
          <button type="submit">Register</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const username = ref("")
const email = ref("")
const password = ref("")
const role = ref("")

const register = async () => {

    await axios.post(
        "http://127.0.0.1:5000/register", {
            username: username.value,
            email: email.value,
            password: password.value,
            role: role.value
        }
    )

    alert("Registration successful")

    window.location.href="/"

}
</script>