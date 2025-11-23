<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const goToSignUp = () => {
  router.push({ name: 'sign-up' })
}

const goToSignIn = () => {
  router.push({ name: 'sign-in' })
}

const goToHome = () => {
  router.push({ name: 'home-page' })
}

const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'home-page' })
}

const submitObservation = () => {
  router.push({ name: 'submit-observation' })
}
</script>

<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo" @click="goToHome">
          <div class="logo-icon">⚡</div>
          <h1 class="logo-text">Gamma Ray Burst</h1>
        </div>

        <div class="auth-buttons">
          <template v-if="!authStore.isAuthenticated">
            <button @click="goToSignIn" class="btn btn-secondary">Sign In</button>
            <button @click="goToSignUp" class="btn btn-primary">Sign Up</button>
          </template>
          <template v-else>
            <button @click="submitObservation" class="btn btn-primary">Submit Observation</button>
            <button @click="handleLogout" class="btn btn-secondary">Logout</button>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: linear-gradient(180deg, #0a0e27 0%, #16213e 50%, #1a1a2e 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(138, 43, 226, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 2px solid rgba(138, 43, 226, 0.3);
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(2px 2px at 20% 30%, white, transparent),
    radial-gradient(2px 2px at 60% 70%, rgba(138, 43, 226, 0.8), transparent),
    radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 80% 10%, rgba(138, 43, 226, 0.6), transparent),
    radial-gradient(2px 2px at 90% 60%, white, transparent),
    radial-gradient(1px 1px at 33% 85%, white, transparent),
    radial-gradient(1px 1px at 15% 75%, rgba(138, 43, 226, 0.7), transparent);
  background-size: 200% 200%;
  background-position: 0% 0%;
  opacity: 0.5;
  animation: twinkle 8s ease-in-out infinite;
  pointer-events: none;
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.25rem 1rem;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: opacity 0.3s ease;
}

.logo:hover {
  opacity: 0.8;
}

.logo-icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 10px rgba(138, 43, 226, 0.8));
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    filter: drop-shadow(0 0 10px rgba(138, 43, 226, 0.8));
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
    filter: drop-shadow(0 0 20px rgba(138, 43, 226, 1));
  }
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(138, 43, 226, 0.5);
}

.auth-buttons {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn {
  padding: 0.625rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  outline: none;
  white-space: nowrap;
}

.btn-primary {
  background: linear-gradient(135deg, #8a2be2 0%, #5a189a 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #9d4edd 0%, #6b1fb1 100%);
  box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid rgba(138, 43, 226, 0.6);
}

.btn-secondary:hover {
  background: rgba(138, 43, 226, 0.1);
  border-color: rgba(138, 43, 226, 0.8);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .logo {
    justify-content: center;
  }

  .logo-text {
    font-size: 1.25rem;
  }

  .auth-buttons {
    justify-content: center;
  }
}
</style>
