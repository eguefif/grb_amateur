<script setup lang="ts">
import { ref } from 'vue'
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
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Form fields
const coordinates = ref('')
const referenceSystem = ref('')
const equinox = ref('')
const wavelengthRange = ref('')
const instrument = ref('')
const magnitude = ref('')
const observationTime = ref('')
const imageFile = ref<File | null>(null)

// Local state
const validationError = ref('')

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    imageFile.value = target.files[0]
  }
}

const handleSubmit = () => {
  validationError.value = ''

  // Basic validation
  if (!props.selectedEvent) {
    validationError.value = 'Please select a GRB event'
    return
  }

  if (!coordinates.value || !referenceSystem.value || !wavelengthRange.value ||
      !instrument.value || !magnitude.value || !observationTime.value) {
    validationError.value = 'Please fill in all required fields'
    return
  }

  // Prepare form data
  const formData = new FormData()
  formData.append('eventId', String(props.selectedEvent.id))
  formData.append('coordinates', coordinates.value)
  formData.append('referenceSystem', referenceSystem.value)
  formData.append('equinox', equinox.value)
  formData.append('wavelengthRange', wavelengthRange.value)
  formData.append('instrument', instrument.value)
  formData.append('magnitude', magnitude.value)
  formData.append('observationTime', observationTime.value)
  if (imageFile.value) formData.append('image', imageFile.value)

  emit('submit', formData)
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="observation-form">
    <div class="form-section">
      <h2 class="section-title">Observation Details</h2>

      <div v-if="validationError" class="validation-error">
        {{ validationError }}
      </div>

      <div class="form-group">
        <label for="coordinates" class="label">
          Best Available Coordinates <span class="required">*</span>
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
        <p class="help-text">Provide the most accurate coordinates you obtained</p>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="referenceSystem" class="label">
            Celestial Reference System/Frame <span class="required">*</span>
          </label>
          <input
            id="referenceSystem"
            v-model="referenceSystem"
            type="text"
            class="input"
            placeholder="e.g., ICRS, J2000, FK5"
            :disabled="isSubmitting"
            required
          />
        </div>

        <div class="form-group">
          <label for="equinox" class="label">
            Equinox and Epoch
          </label>
          <input
            id="equinox"
            v-model="equinox"
            type="text"
            class="input"
            placeholder="e.g., J2000.0, B1950.0"
            :disabled="isSubmitting"
          />
          <p class="help-text">Specify if necessary for your reference system</p>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="wavelengthRange" class="label">
            Wavelength Range <span class="required">*</span>
          </label>
          <input
            id="wavelengthRange"
            v-model="wavelengthRange"
            type="text"
            class="input"
            placeholder="e.g., Optical (400-700nm), UV, IR"
            :disabled="isSubmitting"
            required
          />
          <p class="help-text">Range from which astrometry is obtained</p>
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
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="magnitude" class="label">
            Magnitude <span class="required">*</span>
          </label>
          <input
            id="magnitude"
            v-model="magnitude"
            type="text"
            class="input"
            placeholder="e.g., R=18.5±0.2 mag"
            :disabled="isSubmitting"
            required
          />
          <p class="help-text">Clarify the magnitude and band/filter used</p>
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

    <div class="form-actions">
      <button type="button" @click="handleCancel" class="button button-secondary" :disabled="isSubmitting">
        Cancel
      </button>
      <button type="submit" class="button button-primary" :disabled="isSubmitting || !selectedEvent">
        {{ isSubmitting ? 'Submitting...' : 'Submit Observation' }}
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
