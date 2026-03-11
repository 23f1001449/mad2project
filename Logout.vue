<template>
  <div>
    <h2>Logging out...</h2>
  </div>
</template>

<script>

export default {

  mounted() {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    window.dispatchEvent(new Event("login-status-changed"))
    this.$router.push("/")
  }

}

</script>