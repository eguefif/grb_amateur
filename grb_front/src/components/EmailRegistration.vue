<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const handleSubmit = async () => {
  message.value = ''
  messageType.value = ''

  if (!email.value) {
    message.value = 'Please enter your email address'
    messageType.value = 'error'
    return
  }

  if (!validateEmail(email.value)) {
    message.value = 'Please enter a valid email address'
    messageType.value = 'error'
    return
  }

  isSubmitting.value = true

  try {
    await axios.post('/users/', {
      email: email.value
    })

    message.value = 'Successfully registered for GRB notifications!'
    messageType.value = 'success'
    email.value = ''
  } catch (error) {
    message.value = 'An error occurred. Please try again.'
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="email-registration">
    <div class="container">
      <h1 class="title">Gamma Ray Burst Alert Registration</h1>
      <p class="subtitle">
        Register your email to receive notifications when the Fermi Satellite detects a Gamma Ray
        Burst event
      </p>

      <form @submit.prevent="handleSubmit" class="form">
        <div class="form-group">
          <label for="email" class="label">Email Address</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="input"
            placeholder="your.email@example.com"
            :disabled="isSubmitting"
            autocomplete="email"
          />
        </div>

        <button type="submit" class="button" :disabled="isSubmitting">
          {{ isSubmitting ? 'Registering...' : 'Register for Alerts' }}
        </button>

        <div v-if="message" :class="['message', messageType]">
          {{ message }}
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.email-registration {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 500px;
  width: 100%;
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  color: #718096;
  text-align: center;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label {
  font-weight: 500;
  color: #2d3748;
  font-size: 0.875rem;
}

.input {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  outline: none;
}

.input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
}

.button {
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  outline: none;
}

.button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.button:active:not(:disabled) {
  transform: translateY(0);
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
}

.message.success {
  background-color: #c6f6d5;
  color: #22543d;
  border: 1px solid #9ae6b4;
}

.message.error {
  background-color: #fed7d7;
  color: #742a2a;
  border: 1px solid #fc8181;
}
</style>
