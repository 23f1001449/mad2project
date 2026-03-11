



<template> 
    <div class="login-container">
    
        <h2>Login</h2>
        
        <form @submit.prevent="login">
          <div class="form-group">
            <label>Email</label>
            <input v-model="email" type="email" placeholder="Email" required />
          </div>
      
          <div class="form-group">
            <label>Password</label>
            <input v-model="password" type="password" placeholder="Password" required />
          </div>
      
          <button type="submit">Login</button>
        </form>
    
    </div>
</template>

<script>
import axios from "axios"
export default {
    data() {
        return {
            email: "",
            password: ""
        }
    },

    methods: {
        async login() {
    try {
        const res = await axios.post("http://127.0.0.1:5000/login", {
            email: this.email,
            password: this.password
        })

        localStorage.setItem("token", res.data.access_token)
        localStorage.setItem("role", res.data.role)
        window.dispatchEvent(new Event("login-status-changed"))

        const user = res.data
        

        if(user.role === "student") {
            this.$router.push("/studentdashboard")  // or /profile if you prefer
        } else if(user.role === "company") {
            this.$router.push("/company/dashboard")  // redirect to company dashboard
        } else if(user.role === "admin") {
            this.$router.push("/admindashboard")  // admin dashboard
        }

    } catch (err) {
        console.error(err)
        alert("Login failed")
    }
}
        
    }
}
</script>