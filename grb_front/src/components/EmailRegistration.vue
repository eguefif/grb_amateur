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

    message.value = 'Successfully registered!'
    messageType.value = 'success'
    email.value = ''

    // Clear success message after 5 seconds
    setTimeout(() => {
      message.value = ''
      messageType.value = ''
    }, 5000)
  } catch (error) {
    message.value = 'Registration failed. Please try again.'
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="registration-section">
    <form @submit.prevent="handleSubmit" class="registration-form">
      <input
        v-model="email"
        type="email"
        class="email-input"
        placeholder="your.email@example.com"
        :disabled="isSubmitting"
        autocomplete="email"
      />
      <button type="submit" class="submit-button" :disabled="isSubmitting">
        {{ isSubmitting ? 'Registering...' : 'Get Alerts' }}
      </button>
    </form>

    <transition name="fade">
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>
    </transition>
  </div>
</template>

<style scoped>
.registration-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
  max-width: 500px;
}

.registration-form {
  display: flex;
  gap: 0.5rem;
}

.email-input {
  flex: 1;
  padding: 0.625rem 1rem;
  border: 2px solid rgba(138, 43, 226, 0.4);
  border-radius: 8px;
  font-size: 0.875rem;
  background: rgba(26, 26, 46, 0.6);
  color: #fff;
  transition: all 0.2s;
  outline: none;
  min-width: 0;
  backdrop-filter: blur(10px);
}

.email-input::placeholder {
  color: rgba(177, 156, 217, 0.6);
}

.email-input:focus {
  border-color: #8a2be2;
  background: rgba(26, 26, 46, 0.8);
  box-shadow: 0 0 15px rgba(138, 43, 226, 0.4);
}

.email-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-button {
  padding: 0.625rem 1.5rem;
  background: linear-gradient(135deg, #8a2be2 0%, #4b0082 100%);
  color: white;
  border: 2px solid rgba(138, 43, 226, 0.5);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  outline: none;
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.3);
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(138, 43, 226, 0.6);
  border-color: #8a2be2;
}

.submit-button:active:not(:disabled) {
  transform: translateY(0);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
  backdrop-filter: blur(10px);
}

.message.success {
  background-color: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
  border: 1px solid rgba(16, 185, 129, 0.4);
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
}

.message.error {
  background-color: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .registration-section {
    max-width: 100%;
  }

  .registration-form {
    flex-direction: column;
  }
}
</style>
