<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Please fill in all fields'
    return
  }

  isLoading.value = true

  try {
    // Create form data for OAuth2 password flow
    const formData = new URLSearchParams()
    formData.append('grant_type', 'password')
    formData.append('username', email.value)
    formData.append('password', password.value)

    const response = await axios.post('/users/token', formData.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    // Store the access token and user email
    authStore.setAuth(response.data.access_token, email.value)

    // Redirect to home page
    router.push({ name: 'home-page' })
  } catch {
    errorMessage.value = 'Invalid email or password. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="sign-in-page">
    <div class="sign-in-container">
      <div class="sign-in-card">
        <h1 class="title">Welcome Back</h1>
        <p class="subtitle">Sign in to access your GRB alerts dashboard</p>

        <form @submit.prevent="handleSubmit" class="sign-in-form">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="your@email.com"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="Enter password"
              required
              :disabled="isLoading"
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button type="submit" class="btn-submit" :disabled="isLoading">
            {{ isLoading ? 'Signing In...' : 'Sign In' }}
          </button>
        </form>

        <div class="sign-up-link">
          Don't have an account?
          <router-link to="/sign-up" class="link">Sign Up</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sign-in-page {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(180deg, #0a0e27 0%, #16213e 50%, #1a1a2e 100%);
  min-height: calc(100vh - 100px);
}

.sign-in-container {
  width: 100%;
  max-width: 480px;
}

.sign-in-card {
  background: rgba(26, 26, 46, 0.9);
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.3);
  border: 1px solid rgba(138, 43, 226, 0.2);
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
  text-align: center;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  margin: 0 0 2rem 0;
  font-size: 0.95rem;
}

.sign-in-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
}

.form-group input {
  padding: 0.875rem 1rem;
  border-radius: 8px;
  border: 2px solid rgba(138, 43, 226, 0.3);
  background: rgba(16, 16, 30, 0.8);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.form-group input:focus {
  border-color: rgba(138, 43, 226, 0.8);
  box-shadow: 0 0 0 3px rgba(138, 43, 226, 0.1);
}

.form-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.error-message {
  padding: 0.875rem;
  background: rgba(220, 38, 38, 0.1);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 0.9rem;
}

.btn-submit {
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  outline: none;
  background: linear-gradient(135deg, #8a2be2 0%, #5a189a 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #9d4edd 0%, #6b1fb1 100%);
  box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
  transform: translateY(-2px);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.sign-up-link {
  text-align: center;
  margin-top: 1.5rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
}

.link {
  color: #8a2be2;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link:hover {
  color: #9d4edd;
}

@media (max-width: 480px) {
  .sign-in-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.75rem;
  }
}
</style>
