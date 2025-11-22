<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ObservationList from '@/components/ObservationList.vue'
import { useEventsStore } from '@/stores/events'

const route = useRoute()
const router = useRouter()
const eventsStore = useEventsStore()

const eventId = computed(() => Number(route.params.id))
const event = computed(() => eventsStore.getEventById(eventId.value))

const goBack = () => {
  router.push({ name: 'home' })
}
</script>

<template>
  <div class="event-detail">
    <div class="container">
      <button @click="goBack" class="back-button">← Back to Events</button>

      <div v-if="event" class="content">
        <div class="event-info">
          <h1 class="event-title">GRB Event: Trigger #{{ event.trigger_num }}</h1>
          <p class="event-notice-type">{{ event.notice_type }}</p>

          <div class="event-details-grid">
            <div class="detail-card">
              <span class="detail-label">Date</span>
              <span class="detail-value">{{ event.grb_date }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Time</span>
              <span class="detail-value">{{ event.grb_time }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Significance</span>
              <span class="detail-value">{{ event.trigger_signif }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Duration</span>
              <span class="detail-value">{{ event.trigger_dur }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Energy Range</span>
              <span class="detail-value">{{ event.e_range }}</span>
            </div>
            <div v-if="event.detectors" class="detail-card">
              <span class="detail-label">Detectors</span>
              <span class="detail-value">{{ event.detectors }}</span>
            </div>
            <div v-if="event.algorithm" class="detail-card">
              <span class="detail-label">Algorithm</span>
              <span class="detail-value">{{ event.algorithm }}</span>
            </div>
            <div class="detail-card">
              <span class="detail-label">Notice Date</span>
              <span class="detail-value">{{ event.notice_date }}</span>
            </div>
          </div>

          <div v-if="event.comments" class="comments-section">
            <h3 class="section-title">Comments</h3>
            <p class="comments-text">{{ event.comments }}</p>
          </div>

          <div v-if="event.lc_url" class="light-curve-section">
            <a :href="event.lc_url" target="_blank" class="light-curve-button">
              View Light Curve →
            </a>
          </div>
        </div>

        <div class="observations-container">
          <ObservationList :alert-id="event.id" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.event-detail {
  min-height: 100vh;
  padding: 2rem 1rem;
  background: linear-gradient(180deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
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
}

.back-button:hover {
  border-color: rgba(138, 43, 226, 0.7);
  background: rgba(138, 43, 226, 0.2);
  transform: translateX(-4px);
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
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state {
  text-align: center;
  padding: 4rem 2rem;
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

.content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.event-info {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(138, 43, 226, 0.3);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.event-title {
  font-size: 2rem;
  font-weight: 700;
  color: #b19cd9;
  margin-bottom: 0.5rem;
}

.event-notice-type {
  font-size: 1rem;
  color: rgba(177, 156, 217, 0.7);
  font-style: italic;
  margin-bottom: 2rem;
}

.event-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.detail-card {
  background: rgba(26, 26, 46, 0.6);
  border: 1px solid rgba(138, 43, 226, 0.3);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-label {
  font-size: 0.875rem;
  color: rgba(177, 156, 217, 0.7);
  font-weight: 500;
}

.detail-value {
  font-size: 1rem;
  color: rgba(177, 156, 217, 0.95);
  font-weight: 600;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #b19cd9;
  margin-bottom: 1rem;
}

.comments-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(26, 26, 46, 0.4);
  border-radius: 8px;
  border: 1px solid rgba(138, 43, 226, 0.2);
}

.comments-text {
  color: rgba(177, 156, 217, 0.9);
  line-height: 1.6;
  white-space: pre-wrap;
}

.light-curve-section {
  display: flex;
  justify-content: center;
}

.light-curve-button {
  display: inline-block;
  background: rgba(138, 43, 226, 0.8);
  color: white;
  text-decoration: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  border: 2px solid rgba(138, 43, 226, 0.5);
  transition: all 0.3s;
}

.light-curve-button:hover {
  background: rgba(138, 43, 226, 1);
  border-color: #8a2be2;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.5);
}

.observations-container {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .event-detail {
    padding: 1rem;
  }

  .event-title {
    font-size: 1.5rem;
  }

  .event-details-grid {
    grid-template-columns: 1fr;
  }
}
</style>
