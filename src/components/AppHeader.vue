<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand company-logo" href="/">
          <span class="material-icons-outlined">camera</span>
          <span>Photogram</span>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto"  v-if="currentUser">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link active">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="`/users/${userId}`">My Profile</RouterLink>
            </li>
            <li class="nav-item mr-auto">
              <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
            </li>
            
          </ul>
          <ul class="navbar-nav ms-auto" v-else>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">Login</RouterLink>
            </li>
             <li class="nav-item">
              <RouterLink to="/register" class="nav-link register-link">Register</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
/* Add any component specific styles here */
.company-logo{
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>