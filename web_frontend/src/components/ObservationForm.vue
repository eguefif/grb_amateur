<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import type { GRBEvent } from './GRBEventSelector.vue'

// Props
interface Props {
  selectedEvent: GRBEvent | null
  isSubmitting: boolean
}

// Emits
interface Emits {
  (e: 'submit', formData: FormData): void
  (e: 'cancel'): void
  (e: 'update:isSubmitting', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()
const authStore = useAuthStore()

// Form fields - simplified to match new model
const coordinates = ref('')
const coordinateSystem = ref('')
const instrument = ref('')
const observationTime = ref('')
const imageFile = ref<File | null>(null)
const imagePreview = ref<string | null>(null)

// Local state
const validationError = ref('')
const successMessage = ref('')
const isUploadingImage = ref(false)

const handleSubmit = async () => {
  validationError.value = ''
  successMessage.value = ''

  // Basic validation
  if (!props.selectedEvent) {
    validationError.value = 'Please select a GRB event'
    return
  }

  if (!coordinates.value || !coordinateSystem.value || !instrument.value || !observationTime.value) {
    validationError.value = 'Please fill in all required fields'
    return
  }

  // Image file validation (optional but recommended)
  if (imageFile.value) {
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (imageFile.value.size > maxSize) {
      validationError.value = 'Image file size must be less than 10MB'
      return
    }

    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
    if (!allowedTypes.includes(imageFile.value.type)) {
      validationError.value = 'Image must be JPEG, PNG, GIF, or WebP format'
      return
    }
  }

  // Prepare observation data as JSON (without image)
  const observationData = {
    coordinates: coordinates.value,
    coordinate_sytem: coordinateSystem.value,
    instrument: instrument.value,
    observed_time: observationTime.value,
    alert_id: props.selectedEvent.id
  }

  try {
    emit('update:isSubmitting', true)
    // Step 1: Submit observation data (without image)
    const response = await axios.post('/api/observations/', observationData, {
      headers: {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        ...authStore.getAuthHeader()
      }
    })

    // Get the observation ID from the response
    const observationId = response.data.id

    // Step 2: Upload image if one was selected
    if (imageFile.value && observationId) {
      try {
        isUploadingImage.value = true
        const imageFormData = new FormData()
        imageFormData.append('file', imageFile.value)

        await axios.post(`/api/observations/image/${observationId}`, imageFormData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'accept': 'application/json',
            ...authStore.getAuthHeader()
          }
        })

        successMessage.value = 'Observation and image submitted successfully!'
      } catch (imageError) {
        // Observation was created but image upload failed
        console.error('Image upload failed:', imageError)
        successMessage.value = 'Observation submitted successfully, but image upload failed.'
      } finally {
        isUploadingImage.value = false
        emit('update:isSubmitting', false)
      }
    } else {
      successMessage.value = 'Observation submitted successfully!'
      emit('update:isSubmitting', false)
    }

    // Reset form
    coordinates.value = ''
    coordinateSystem.value = ''
    instrument.value = ''
    observationTime.value = ''
    imageFile.value = null
    imagePreview.value = null

    // Notify parent component of success after a brief delay
    setTimeout(() => {
      emit('cancel')
    }, 2000)

  } catch (error) {
    emit('update:isSubmitting', false)
    if (axios.isAxiosError(error) && error.response) {
      validationError.value = error.response.data.detail || 'Failed to submit observation'
    } else {
      validationError.value = 'Failed to submit observation'
    }
  }
}

const handleCancel = () => {
  emit('cancel')
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (file) {
    imageFile.value = file

    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
}

const clearImage = () => {
  imageFile.value = null
  imagePreview.value = null
  // Reset file input
  const fileInput = document.getElementById('imageFile') as HTMLInputElement
  if (fileInput) {
    fileInput.value = ''
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="observation-form">
    <div class="form-section">
      <h2 class="section-title">Observation Details</h2>

      <div v-if="validationError" class="validation-error">
        {{ validationError }}
      </div>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div class="form-group">
        <label for="coordinates" class="label">
          Coordinates <span class="required">*</span>
        </label>
        <input
          id="coordinates"
          v-model="coordinates"
          type="text"
          class="input"
          placeholder="e.g., RA: 12h 34m 56.7s, Dec: +45° 12' 34.5&quot;"
          :disabled="isSubmitting"
          required
        />
        <p class="help-text">Provide the coordinates you obtained</p>
      </div>

      <div class="form-group">
        <label for="coordinateSystem" class="label">
          Coordinate System <span class="required">*</span>
        </label>
        <select
          id="coordinateSystem"
          v-model="coordinateSystem"
          class="input"
          :disabled="isSubmitting"
          required
        >
          <option value="" disabled>Select a coordinate system</option>
          <option value="icrs_j2000">ICRS/J2000</option>
          <option value="fk5_j2000">FK5/J2000</option>
          <option value="b1950">B1950</option>
          <option value="galactic">Galactic</option>
          <option value="current_equinox">Current Equinox</option>
        </select>
        <p class="help-text">Specify the coordinate system/reference frame used</p>
      </div>

      <div class="form-group">
        <label for="instrument" class="label">
          Instrument <span class="required">*</span>
        </label>
        <input
          id="instrument"
          v-model="instrument"
          type="text"
          class="input"
          placeholder="e.g., Schmidt-Cassegrain 14&quot; + CCD"
          :disabled="isSubmitting"
          required
        />
        <p class="help-text">Describe your observation instrument</p>
      </div>

      <div class="form-group">
        <label for="observationTime" class="label">
          Time of Observation <span class="required">*</span>
        </label>
        <input
          id="observationTime"
          v-model="observationTime"
          type="datetime-local"
          class="input"
          :disabled="isSubmitting"
          required
        />
      </div>

      <div class="form-group">
        <label for="imageFile" class="label">
          Observation Image
        </label>
        <div class="file-input-wrapper">
          <input
            id="imageFile"
            type="file"
            accept="image/*"
            class="file-input"
            @change="handleFileChange"
            :disabled="isSubmitting"
          />
          <label for="imageFile" class="file-input-label">
            <span class="file-input-icon">📷</span>
            <span class="file-input-text">
              {{ imageFile ? imageFile.name : 'Choose an image file' }}
            </span>
          </label>
          <button
            v-if="imageFile"
            type="button"
            @click="clearImage"
            class="clear-image-btn"
            :disabled="isSubmitting"
          >
            ✕
          </button>
        </div>
        <p class="help-text">Optional: Upload an image of your observation (JPEG, PNG, GIF, WebP - Max 10MB)</p>

        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="Image preview" />
        </div>
      </div>
    </div>

    <div class="form-actions">
      <button type="button" @click="handleCancel" class="button button-secondary" :disabled="isSubmitting || isUploadingImage">
        Return to Homepage
      </button>
      <button type="submit" class="button button-primary" :disabled="isSubmitting || isUploadingImage || !selectedEvent">
        {{ isUploadingImage ? 'Uploading Image...' : (isSubmitting ? 'Submitting...' : 'Submit Observation') }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.observation-form {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(138, 43, 226, 0.3);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.form-section {
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

.validation-error {
  background-color: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.success-message {
  background-color: rgba(34, 197, 94, 0.2);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.4);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
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

.help-text {
  font-size: 0.75rem;
  color: rgba(177, 156, 217, 0.7);
  margin-top: -0.25rem;
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

/* File input styles */
.file-input-wrapper {
  position: relative;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.file-input {
  position: absolute;
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  z-index: -1;
}

.file-input-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 2px solid rgba(138, 43, 226, 0.4);
  border-radius: 8px;
  background: rgba(26, 26, 46, 0.6);
  color: rgba(177, 156, 217, 0.9);
  cursor: pointer;
  transition: all 0.2s;
  flex: 1;
  min-width: 0;
}

.file-input-label:hover {
  border-color: #8a2be2;
  background: rgba(26, 26, 46, 0.8);
  box-shadow: 0 0 15px rgba(138, 43, 226, 0.4);
}

.file-input:disabled + .file-input-label {
  opacity: 0.6;
  cursor: not-allowed;
}

.file-input-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.file-input-text {
  font-size: 0.875rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.clear-image-btn {
  padding: 0.5rem 0.75rem;
  background: rgba(239, 68, 68, 0.2);
  border: 2px solid rgba(239, 68, 68, 0.4);
  border-radius: 8px;
  color: #fca5a5;
  cursor: pointer;
  font-size: 1.25rem;
  font-weight: bold;
  transition: all 0.2s;
  flex-shrink: 0;
}

.clear-image-btn:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.3);
  border-color: rgba(239, 68, 68, 0.6);
}

.clear-image-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.image-preview {
  margin-top: 1rem;
  border: 2px solid rgba(138, 43, 226, 0.3);
  border-radius: 8px;
  overflow: hidden;
  background: rgba(26, 26, 46, 0.4);
  max-width: 500px;
}

.image-preview img {
  width: 100%;
  height: auto;
  display: block;
}

@media (max-width: 768px) {
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

  .file-input-wrapper {
    flex-direction: column;
    align-items: stretch;
  }

  .clear-image-btn {
    width: 100%;
  }

  .image-preview {
    max-width: 100%;
  }
}
</style>
