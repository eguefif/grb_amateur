<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

// GRB Event interface
export interface GRBEvent {
  id: number
  trigger_num: number
  notice_date: string
  grb_date: string
  grb_time: string
  notice_type: string
  trigger_signif: string
  trigger_dur: string
  e_range: string
  comments: string
  lc_url: string
  title?: string
  record_num?: number
  detectors?: string
  algorithm?: string
}

// Props
interface Props {
  modelValue: GRBEvent | null
}

// Emits
interface Emits {
  (e: 'update:modelValue', value: GRBEvent | null): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// State
const events = ref<GRBEvent[]>([])
const isLoadingEvents = ref(false)
const errorMessage = ref('')

// Fetch last 5 GRB events
const fetchEvents = async () => {
  isLoadingEvents.value = true
  errorMessage.value = ''
  try {
    const response = await axios.get('/events/last_events')
    events.value = response.data
  } catch (error) {
    errorMessage.value = 'Failed to load recent GRB events'
    console.error('Error fetching events:', error)
  } finally {
    isLoadingEvents.value = false
  }
}

// Select or unselect event
const selectEvent = (event: GRBEvent) => {
  // If clicking on the already selected event, unselect it
  if (props.modelValue?.id === event.id) {
    emit('update:modelValue', null)
  } else {
    emit('update:modelValue', event)
  }
}

onMounted(() => {
  fetchEvents()
})
</script>

<template>
  <div class="events-section">
    <h2 class="section-title">Select GRB Event</h2>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <div v-if="isLoadingEvents" class="loading">Loading recent events...</div>

    <div v-else-if="events.length === 0 && !errorMessage" class="no-events">
      No recent GRB events available
    </div>

    <div v-else class="event-cards">
      <div
        v-for="event in events"
        :key="event.id"
        :class="['event-card', { active: modelValue?.id === event.id }]"
        @click="selectEvent(event)"
      >
        <div class="event-header">
          <h3 class="event-trigger">Trigger #{{ event.trigger_num }}</h3>
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
            <span class="detail-label">Energy:</span>
            <span class="detail-value">{{ event.e_range }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.events-section {
  margin-bottom: 2rem;
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(138, 43, 226, 0.3);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #b19cd9;
  margin-bottom: 1.25rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(138, 43, 226, 0.3);
}

.loading,
.no-events {
  text-align: center;
  color: rgba(177, 156, 217, 0.9);
  padding: 2rem;
  font-size: 1rem;
}

.error-message {
  background-color: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.event-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.event-card {
  background: rgba(26, 26, 46, 0.6);
  border: 2px solid rgba(138, 43, 226, 0.4);
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.event-card:hover {
  border-color: rgba(138, 43, 226, 0.7);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.3);
}

.event-card.active {
  border-color: #8a2be2;
  background: rgba(138, 43, 226, 0.2);
  box-shadow: 0 0 25px rgba(138, 43, 226, 0.5);
}

.event-card.active::before {
  content: '✓';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  color: #8a2be2;
  font-size: 1.5rem;
  font-weight: bold;
}

.event-header {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(138, 43, 226, 0.3);
}

.event-trigger {
  font-size: 1.125rem;
  font-weight: 600;
  color: #b19cd9;
  margin: 0;
}

.event-type {
  font-size: 0.75rem;
  color: rgba(177, 156, 217, 0.7);
  font-style: italic;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.event-detail-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  font-size: 0.875rem;
  gap: 0.5rem;
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

@media (max-width: 768px) {
  .events-section {
    padding: 1.5rem;
  }

  .event-cards {
    grid-template-columns: 1fr;
  }
}
</style>
