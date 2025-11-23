<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const email = ref('')
const fullName = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  errorMessage.value = ''

  if (!email.value || !fullName.value || !password.value || !confirmPassword.value) {
    errorMessage.value = 'Please fill in all fields'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  if (password.value.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long'
    return
  }

  isLoading.value = true

  try {
    const userData = {
      email: email.value,
      full_name: fullName.value,
      email_confirmed: false,
      password: password.value,
      password_confirmation: confirmPassword.value
    }

    await axios.post('/users/', userData, {
      headers: {
        'Content-Type': 'application/json'
      }
    })

    // Redirect to sign in after successful registration
    router.push({ name: 'sign-in' })
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      errorMessage.value = error.response.data.detail || 'An error occurred during sign up. Please try again.'
    } else {
      errorMessage.value = 'An error occurred during sign up. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="sign-up-page">
    <div class="sign-up-container">
      <div class="sign-up-card">
        <h1 class="title">Create Account</h1>
        <p class="subtitle">Sign up to receive GRB alerts and submit observations</p>

        <form @submit.prevent="handleSubmit" class="sign-up-form">
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
            <label for="full-name">Full Name</label>
            <input
              id="full-name"
              v-model="fullName"
              type="text"
              placeholder="John Doe"
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
              placeholder="Enter password (min. 8 characters)"
              required
              :disabled="isLoading"
            />
          </div>

          <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <input
              id="confirm-password"
              v-model="confirmPassword"
              type="password"
              placeholder="Confirm password"
              required
              :disabled="isLoading"
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button type="submit" class="btn-submit" :disabled="isLoading">
            {{ isLoading ? 'Creating Account...' : 'Sign Up' }}
          </button>
        </form>

        <div class="sign-in-link">
          Already have an account?
          <router-link to="/sign-in" class="link">Sign In</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sign-up-page {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(180deg, #0a0e27 0%, #16213e 50%, #1a1a2e 100%);
  min-height: calc(100vh - 100px);
}

.sign-up-container {
  width: 100%;
  max-width: 480px;
}

.sign-up-card {
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

.sign-up-form {
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

.sign-in-link {
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
  .sign-up-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.75rem;
  }
}
</style>
