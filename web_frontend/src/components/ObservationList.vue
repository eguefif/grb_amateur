<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import ObservationCard from './ObservationCard.vue'
import type { GrbObservation } from '@/types/observation'
import { getObservationsByAlertId } from '@/services/api'

interface Props {
  alertId: number
}

const props = defineProps<Props>()
const router = useRouter()

const observations = ref<GrbObservation[]>([])
const isLoading = ref(false)
const error = ref<string | null>(null)

const fetchObservations = async () => {
  isLoading.value = true
  error.value = null
  try {
    observations.value = await getObservationsByAlertId(props.alertId)
  } catch (err) {
    error.value = 'Failed to load observations. Please try again later.'
    console.error('Error fetching observations:', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchObservations()
})

watch(() => props.alertId, () => {
  fetchObservations()
})

const goBack = () => {
  router.push({ name: 'home-page' })
}
</script>

<template>
  <div class="observation-list">
    <div class="container">
      <button @click="goBack" class="back-button">← Back to Events</button>

      <h2 class="section-title">Observations for this Event</h2>
      <p class="section-subtitle">
        Amateur astronomer observations of this Gamma Ray Burst event
      </p>

      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Loading observations...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchObservations" class="retry-button">Retry</button>
      </div>

      <div v-else-if="observations.length === 0" class="empty-state">
        <p>No observations available yet. Be the first to submit one!</p>
      </div>

      <div v-else class="cards-grid">
        <ObservationCard
          v-for="observation in observations"
          :key="observation.id"
          :observation="observation"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.observation-list {
  padding: 2rem 1rem;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
  min-height: calc(100vh - 80px);
  position: relative;
  overflow: hidden;
}

.observation-list::before {
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
    radial-gradient(2px 2px at 50% 90%, white, transparent),
    radial-gradient(1px 1px at 85% 35%, white, transparent),
    radial-gradient(1px 1px at 15% 65%, rgba(138, 43, 226, 0.7), transparent),
    radial-gradient(2px 2px at 40% 70%, white, transparent),
    radial-gradient(1px 1px at 60% 25%, white, transparent),
    radial-gradient(1px 1px at 30% 85%, rgba(138, 43, 226, 0.6), transparent),
    radial-gradient(2px 2px at 70% 50%, white, transparent),
    radial-gradient(1px 1px at 95% 60%, white, transparent),
    radial-gradient(1px 1px at 5% 40%, rgba(138, 43, 226, 0.5), transparent);
  background-size: 100% 100%;
  opacity: 0.6;
  animation: stars-float 120s linear infinite;
  pointer-events: none;
}

@keyframes stars-float {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-100px);
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 0.5rem;
  text-align: center;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 40px rgba(138, 43, 226, 0.6);
}

.section-subtitle {
  color: rgba(177, 156, 217, 0.9);
  text-align: center;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: rgba(177, 156, 217, 0.8);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(138, 43, 226, 0.2);
  border-top-color: #8a2be2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(177, 156, 217, 0.8);
  font-size: 1.125rem;
}

.error-state {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 100, 100, 0.9);
  font-size: 1.125rem;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #8a2be2 0%, #4b0082 100%);
  color: white;
  border: 2px solid rgba(138, 43, 226, 0.5);
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  outline: none;
  box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(138, 43, 226, 0.7);
  border-color: #8a2be2;
}

.retry-button:active {
  transform: translateY(0);
}

.cards-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.back-button {
  background: rgba(26, 26, 46, 0.8);
  color: #b19cd9;
  border: 2px solid rgba(138, 43, 226, 0.4);
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 2rem;
  outline: none;
}

.back-button:hover {
  border-color: rgba(138, 43, 226, 0.7);
  background: rgba(138, 43, 226, 0.2);
  transform: translateX(-4px);
}

.back-button:active {
  transform: translateX(-2px);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.5rem;
  }
}
</style>
