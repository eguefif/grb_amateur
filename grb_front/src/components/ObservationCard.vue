<script setup lang="ts">
import type { GrbObservation } from '@/types/observation'

defineProps<{
  observation: GrbObservation
}>()

const getPlaceholderImage = (observationId: number) => {
  const colors = ['667eea', '764ba2', '8a2be2', '4b0082', '9b59b6']
  const color = colors[observationId % colors.length]
  return `https://placehold.co/400x300/${color}/white?text=Observation+${observationId}`
}
</script>

<template>
  <div class="observation-card">
    <div class="card-image">
      <img :src="getPlaceholderImage(observation.id)" :alt="`Observation ${observation.id}`" />
    </div>
    <div class="card-content">
      <div class="card-header">
        <h3 class="card-title">Observation #{{ observation.id }}</h3>
        <div class="card-datetime">
          <span class="date">Alert ID: {{ observation.alert_id }}</span>
          <span class="time">{{ observation.observed_time }}</span>
        </div>
      </div>
      <div class="card-details">
        <div class="detail-row">
          <span class="label">Coordinates:</span>
          <span class="value">{{ observation.coordinates }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Reference:</span>
          <span class="value">{{ observation.celestial_reference }} ({{ observation.equinox }})</span>
        </div>
        <div class="detail-row">
          <span class="label">Epoch:</span>
          <span class="value">{{ observation.epoch }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Instrument:</span>
          <span class="value">{{ observation.instrument }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Wavelength:</span>
          <span class="value">{{ observation.wave_length }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Magnitude:</span>
          <span class="value">{{ observation.magnitude }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.observation-card {
  display: flex;
  flex-direction: row;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), 0 0 30px rgba(138, 43, 226, 0.2);
  border: 1px solid rgba(138, 43, 226, 0.3);
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
  backdrop-filter: blur(10px);
  min-height: 250px;
}

.observation-card:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 50px rgba(138, 43, 226, 0.5);
  border-color: rgba(138, 43, 226, 0.6);
}

.card-image {
  width: 300px;
  min-width: 300px;
  height: auto;
  overflow: hidden;
  background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
  position: relative;
  border-right: 2px solid rgba(138, 43, 226, 0.4);
}

.card-image::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(10, 14, 39, 0.3) 100%);
  pointer-events: none;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.9;
}

.card-content {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  flex: 1;
}

.card-header {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(138, 43, 226, 0.3);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 20px rgba(138, 43, 226, 0.5);
}

.card-datetime {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: rgba(177, 156, 217, 0.8);
}

.date {
  font-weight: 500;
  color: #b19cd9;
}

.time {
  color: rgba(177, 156, 217, 0.6);
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.detail-row {
  display: flex;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.label {
  font-weight: 600;
  color: #8a2be2;
  min-width: 100px;
  text-shadow: 0 0 10px rgba(138, 43, 226, 0.3);
}

.value {
  color: rgba(255, 255, 255, 0.9);
}

.description {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid rgba(138, 43, 226, 0.3);
  color: rgba(177, 156, 217, 0.9);
  font-size: 0.875rem;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .observation-card {
    flex-direction: column;
    min-height: auto;
  }

  .observation-card:hover {
    transform: translateY(-8px);
  }

  .card-image {
    width: 100%;
    height: 200px;
    border-right: none;
    border-bottom: 2px solid rgba(138, 43, 226, 0.4);
  }

  .card-image::after {
    background: linear-gradient(180deg, transparent 0%, rgba(10, 14, 39, 0.3) 100%);
  }

  .label {
    min-width: 90px;
  }
}
</style>
