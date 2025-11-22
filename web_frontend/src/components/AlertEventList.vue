<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useEventsStore, type GRBEvent } from '@/stores/events'

const router = useRouter()
const eventsStore = useEventsStore()

const isLoading = ref(false)
const error = ref<string | null>(null)

const events = computed(() => eventsStore.events)

const fetchEvents = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await axios.get('/events/last_events')
    const sortedEvents = response.data.sort((a: GRBEvent, b: GRBEvent) => {
      const dateA = new Date(`${a.grb_date} ${a.grb_time}`)
      const dateB = new Date(`${b.grb_date} ${b.grb_time}`)
      return dateB.getTime() - dateA.getTime()
    })
    eventsStore.setEvents(sortedEvents)
  } catch (err) {
    error.value = 'Failed to load recent GRB events. Please try again later.'
    console.error('Error fetching events:', err)
  } finally {
    isLoading.value = false
  }
}

const selectEvent = (event: GRBEvent) => {
  router.push({
    name: 'event-detail',
    params: { id: event.id }
  })
}

const goToSubmitObservation = () => {
  router.push({ name: 'submit-observation' })
}

onMounted(() => {
  fetchEvents()
})
</script>

<template>
  <div class="alert-events">
    <div class="header-section">
      <div class="header-text">
        <h1 class="title">Recent Gamma Ray Burst Events</h1>
        <p class="subtitle">Last 5 alerts from Fermi Satellite</p>
      </div>
      <button @click="goToSubmitObservation" class="submit-button">
        Submit Observation
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Loading recent events...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchEvents" class="retry-button">Retry</button>
    </div>

    <div v-else-if="events.length === 0" class="empty-state">
      <p>No recent GRB events available</p>
    </div>

    <div v-else class="event-cards">
      <div
        v-for="event in events"
        :key="event.id"
        class="event-card"
        @click="selectEvent(event)"
      >
        <div class="event-header">
          <h2 class="event-trigger">Trigger #{{ event.trigger_num }}</h2>
          <span class="event-type">{{ event.notice_type }}</span>
        </div>
        <div class="event-details">
          <div class="event-detail-row">
            <span class="detail-label">Date:</span>
            <span class="detail-value">{{ event.grb_date }}</span>
          </div>
          <div class="event-detail-row">
            <span class="detail-label">Time:</span>
            <span class="detail-value">{{ event.grb_time }}</span>
          </div>
          <div class="event-detail-row">
            <span class="detail-label">Significance:</span>
            <span class="detail-value">{{ event.trigger_signif }}</span>
          </div>
          <div class="event-detail-row">
            <span class="detail-label">Duration:</span>
            <span class="detail-value">{{ event.trigger_dur }}</span>
          </div>
          <div class="event-detail-row">
            <span class="detail-label">Energy:</span>
            <span class="detail-value">{{ event.e_range }}</span>
          </div>
          <div v-if="event.detectors" class="event-detail-row">
            <span class="detail-label">Detectors:</span>
            <span class="detail-value">{{ event.detectors }}</span>
          </div>
        </div>
        <div v-if="event.lc_url" class="event-footer">
          <a :href="event.lc_url" target="_blank" class="event-link" @click.stop>View Light Curve</a>
        </div>
        <div class="click-hint">Click to view details</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.alert-events {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 2rem;
}

.header-text {
  flex: 1;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #b19cd9;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1rem;
  color: rgba(177, 156, 217, 0.7);
}

.submit-button {
  background: rgba(138, 43, 226, 0.8);
  color: white;
  border: 2px solid rgba(138, 43, 226, 0.5);
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.submit-button:hover {
  background: rgba(138, 43, 226, 1);
  border-color: #8a2be2;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.5);
}

.loading,
.error-state,
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: rgba(177, 156, 217, 0.9);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(138, 43, 226, 0.3);
  border-top-color: #8a2be2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state {
  color: #fca5a5;
}

.error-state p {
  margin-bottom: 1rem;
}

.retry-button {
  background: rgba(138, 43, 226, 0.8);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.retry-button:hover {
  background: rgba(138, 43, 226, 1);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
}

.empty-state {
  color: rgba(177, 156, 217, 0.7);
  font-size: 1.125rem;
}

.event-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.event-card {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(138, 43, 226, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
  cursor: pointer;
  position: relative;
}

.event-card:hover {
  border-color: rgba(138, 43, 226, 0.6);
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(138, 43, 226, 0.3);
}

.click-hint {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(138, 43, 226, 0.2);
  text-align: center;
  font-size: 0.875rem;
  color: rgba(177, 156, 217, 0.6);
  font-style: italic;
}

.event-card:hover .click-hint {
  color: rgba(138, 43, 226, 0.9);
}

.event-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(138, 43, 226, 0.3);
}

.event-trigger {
  font-size: 1.25rem;
  font-weight: 600;
  color: #b19cd9;
  margin: 0;
}

.event-type {
  font-size: 0.875rem;
  color: rgba(177, 156, 217, 0.7);
  font-style: italic;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  margin-bottom: 1rem;
}

.event-detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  font-size: 0.9rem;
  gap: 1rem;
}

.detail-label {
  color: rgba(177, 156, 217, 0.7);
  font-weight: 500;
  white-space: nowrap;
}

.detail-value {
  color: rgba(177, 156, 217, 0.95);
  text-align: right;
  word-break: break-word;
}

.event-footer {
  padding-top: 1rem;
  border-top: 1px solid rgba(138, 43, 226, 0.2);
}

.event-link {
  display: inline-block;
  color: #8a2be2;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s;
}

.event-link:hover {
  color: #b19cd9;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .alert-events {
    padding: 1rem;
  }

  .header-section {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .submit-button {
    width: 100%;
  }

  .event-cards {
    grid-template-columns: 1fr;
  }
}
</style>
