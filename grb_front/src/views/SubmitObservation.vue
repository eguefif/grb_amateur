<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Form fields
const triggerNumber = ref('')
const ra = ref<number | ''>('')
const dec = ref<number | ''>('')
const error = ref<number | ''>('')
const intensity = ref<number | ''>('')
const date = ref('')
const time = ref('')
const observer = ref('')
const telescope = ref('')
const description = ref('')
const imageFile = ref<File | null>(null)

// Form state
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error' | ''>('')

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    imageFile.value = target.files[0]
  }
}

const closeMessage = () => {
  message.value = ''
  messageType.value = ''
}

const handleSubmit = async () => {
  message.value = ''
  messageType.value = ''

  // Basic validation
  if (!triggerNumber.value || ra.value === '' || dec.value === '' ||
      error.value === '' || intensity.value === '' || !date.value || !time.value) {
    message.value = 'Please fill in all required fields'
    messageType.value = 'error'
    return
  }

  isSubmitting.value = true

  try {
    // Prepare form data
    const formData = new FormData()
    formData.append('triggerNumber', triggerNumber.value)
    formData.append('ra', String(ra.value))
    formData.append('dec', String(dec.value))
    formData.append('error', String(error.value))
    formData.append('intensity', String(intensity.value))
    formData.append('date', date.value)
    formData.append('time', time.value)

    if (observer.value) formData.append('observer', observer.value)
    if (telescope.value) formData.append('telescope', telescope.value)
    if (description.value) formData.append('description', description.value)
    if (imageFile.value) formData.append('image', imageFile.value)

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
          Share your Gamma Ray Burst observation with the amateur astronomy community
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="observation-form">
        <div class="form-section">
          <h2 class="section-title">GCN Event Details</h2>

          <div class="form-row">
            <div class="form-group">
              <label for="triggerNumber" class="label">
                Trigger Number <span class="required">*</span>
              </label>
              <input
                id="triggerNumber"
                v-model="triggerNumber"
                type="text"
                class="input"
                placeholder="e.g., 240815A"
                :disabled="isSubmitting"
                required
              />
            </div>

            <div class="form-group">
              <label for="intensity" class="label">
                Intensity <span class="required">*</span>
              </label>
              <input
                id="intensity"
                v-model.number="intensity"
                type="number"
                step="0.1"
                class="input"
                placeholder="e.g., 4.5"
                :disabled="isSubmitting"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="ra" class="label">
                Right Ascension (RA) <span class="required">*</span>
              </label>
              <input
                id="ra"
                v-model.number="ra"
                type="number"
                step="0.01"
                class="input"
                placeholder="e.g., 123.45"
                :disabled="isSubmitting"
                required
              />
            </div>

            <div class="form-group">
              <label for="dec" class="label">
                Declination (Dec) <span class="required">*</span>
              </label>
              <input
                id="dec"
                v-model.number="dec"
                type="number"
                step="0.01"
                class="input"
                placeholder="e.g., -23.67"
                :disabled="isSubmitting"
                required
              />
            </div>

            <div class="form-group">
              <label for="error" class="label">
                Error <span class="required">*</span>
              </label>
              <input
                id="error"
                v-model.number="error"
                type="number"
                step="0.1"
                class="input"
                placeholder="e.g., 3.2"
                :disabled="isSubmitting"
                required
              />
            </div>
          </div>
        </div>

        <div class="form-section">
          <h2 class="section-title">Observation Details</h2>

          <div class="form-row">
            <div class="form-group">
              <label for="date" class="label">
                Date <span class="required">*</span>
              </label>
              <input
                id="date"
                v-model="date"
                type="date"
                class="input"
                :disabled="isSubmitting"
                required
              />
            </div>

            <div class="form-group">
              <label for="time" class="label">
                Time (UTC) <span class="required">*</span>
              </label>
              <input
                id="time"
                v-model="time"
                type="time"
                step="1"
                class="input"
                :disabled="isSubmitting"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="observer" class="label">Observer Name</label>
              <input
                id="observer"
                v-model="observer"
                type="text"
                class="input"
                placeholder="e.g., Dr. Smith Observatory"
                :disabled="isSubmitting"
              />
            </div>

            <div class="form-group">
              <label for="telescope" class="label">Telescope</label>
              <input
                id="telescope"
                v-model="telescope"
                type="text"
                class="input"
                placeholder="e.g., Schmidt-Cassegrain 14&quot;"
                :disabled="isSubmitting"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="description" class="label">Description</label>
            <textarea
              id="description"
              v-model="description"
              class="textarea"
              placeholder="Describe your observation..."
              rows="4"
              :disabled="isSubmitting"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="image" class="label">Image</label>
            <input
              id="image"
              type="file"
              accept="image/*"
              class="file-input"
              @change="handleFileChange"
              :disabled="isSubmitting"
            />
            <p class="help-text">Upload an image of your observation (optional)</p>
          </div>
        </div>

        <transition name="fade">
          <div v-if="message" :class="['message', messageType]">
            <span>{{ message }}</span>
            <button @click="closeMessage" class="close-button" type="button" aria-label="Close message">
              ✕
            </button>
          </div>
        </transition>

        <div class="form-actions">
          <button type="button" @click="handleCancel" class="button button-secondary" :disabled="isSubmitting">
            Cancel
          </button>
          <button type="submit" class="button button-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Submitting...' : 'Submit Observation' }}
          </button>
        </div>
      </form>
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
  max-width: 800px;
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

.observation-form {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(138, 43, 226, 0.3);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.form-section {
  margin-bottom: 2rem;
}

.form-section:last-of-type {
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #b19cd9;
  margin-bottom: 1.25rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(138, 43, 226, 0.3);
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label {
  font-weight: 500;
  color: rgba(177, 156, 217, 0.9);
  font-size: 0.875rem;
}

.required {
  color: #fc8181;
}

.input,
.textarea {
  padding: 0.75rem 1rem;
  border: 2px solid rgba(138, 43, 226, 0.4);
  border-radius: 8px;
  font-size: 0.875rem;
  background: rgba(26, 26, 46, 0.6);
  color: #fff;
  transition: all 0.2s;
  outline: none;
  font-family: inherit;
}

.input::placeholder,
.textarea::placeholder {
  color: rgba(177, 156, 217, 0.5);
}

.input:focus,
.textarea:focus {
  border-color: #8a2be2;
  background: rgba(26, 26, 46, 0.8);
  box-shadow: 0 0 15px rgba(138, 43, 226, 0.4);
}

.input:disabled,
.textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.textarea {
  resize: vertical;
  min-height: 100px;
}

.file-input {
  padding: 0.5rem;
  border: 2px solid rgba(138, 43, 226, 0.4);
  border-radius: 8px;
  background: rgba(26, 26, 46, 0.6);
  color: rgba(177, 156, 217, 0.9);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.file-input:hover:not(:disabled) {
  border-color: #8a2be2;
}

.file-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.help-text {
  font-size: 0.75rem;
  color: rgba(177, 156, 217, 0.7);
  margin-top: -0.25rem;
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

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.button {
  padding: 0.875rem 2rem;
  border: 2px solid rgba(138, 43, 226, 0.5);
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  outline: none;
}

.button-primary {
  background: linear-gradient(135deg, #8a2be2 0%, #4b0082 100%);
  color: white;
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
}

.button-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(138, 43, 226, 0.7);
  border-color: #8a2be2;
}

.button-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-secondary {
  background: rgba(26, 26, 46, 0.6);
  color: rgba(177, 156, 217, 0.9);
  border-color: rgba(138, 43, 226, 0.3);
}

.button-secondary:hover:not(:disabled) {
  background: rgba(26, 26, 46, 0.8);
  border-color: rgba(138, 43, 226, 0.5);
}

.button-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }

  .observation-form {
    padding: 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .button {
    width: 100%;
  }
}
</style>
