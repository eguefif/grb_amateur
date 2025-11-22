<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import GRBEventSelector, { type GRBEvent } from '@/components/GRBEventSelector.vue'
import ObservationForm from '@/components/ObservationForm.vue'

const router = useRouter()

// State
const selectedEvent = ref<GRBEvent | null>(null)
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

const closeMessage = () => {
  message.value = ''
  messageType.value = ''
}

const handleSubmit = async (formData: FormData) => {
  message.value = ''
  messageType.value = ''
  isSubmitting.value = true

  try {
    // TODO: Replace with actual API endpoint
    await axios.post('/observations/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    message.value = 'Observation submitted successfully!'
    messageType.value = 'success'

    // Reset form after successful submission
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 400) {
      message.value = 'Invalid observation data. Please check your inputs.'
      messageType.value = 'error'
    } else {
      message.value = 'Failed to submit observation. Please try again.'
      messageType.value = 'error'
    }
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  router.push('/')
}
</script>

<template>
  <div class="submit-observation">
    <div class="container">
      <div class="header">
        <h1 class="title">Submit GRB Observation</h1>
        <p class="subtitle">
          Select a recent GRB event and share your observation with the amateur astronomy community
        </p>
      </div>

      <GRBEventSelector v-model="selectedEvent" />

      <transition name="fade">
        <div v-if="message" :class="['message', messageType]">
          <span>{{ message }}</span>
          <button @click="closeMessage" class="close-button" type="button" aria-label="Close message">
            ✕
          </button>
        </div>
      </transition>

      <ObservationForm
        :selected-event="selectedEvent"
        :is-submitting="isSubmitting"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </div>
  </div>
</template>

<style scoped>
.submit-observation {
  min-height: 100vh;
  padding: 2rem 1rem;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
  position: relative;
  overflow: hidden;
}

.submit-observation::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(2px 2px at 10% 20%, white, transparent),
    radial-gradient(2px 2px at 90% 80%, white, transparent),
    radial-gradient(1px 1px at 25% 45%, white, transparent),
    radial-gradient(1px 1px at 75% 15%, rgba(138, 43, 226, 0.8), transparent),
    radial-gradient(2px 2px at 50% 90%, white, transparent);
  background-size: 100% 100%;
  opacity: 0.6;
  pointer-events: none;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(138, 43, 226, 0.6);
}

.subtitle {
  color: rgba(177, 156, 217, 0.9);
  font-size: 1.125rem;
  line-height: 1.6;
}

.message {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  text-align: center;
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  color: currentColor;
  cursor: pointer;
  padding: 0;
  font-size: 1rem;
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1rem;
  height: 1rem;
}

.close-button:hover {
  opacity: 1;
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
  .title {
    font-size: 2rem;
  }
}
</style>
