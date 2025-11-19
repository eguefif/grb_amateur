<script setup lang="ts">
import { ref } from 'vue'
import ObservationCard from './ObservationCard.vue'
import type { GrbObservation } from '@/types/observation'

// Mock data for demonstration - this will be replaced with API calls later
const observations = ref<GrbObservation[]>([
  {
    id: '1',
    imageUrl: 'https://placehold.co/400x300/667eea/white?text=GRB+240815A',
    date: '2024-08-15',
    time: '14:23:45 UTC',
    gcnEvent: {
      triggerNumber: '240815A',
      ra: 123.45,
      dec: -23.67,
      error: 3.2,
      intensity: 4.5
    },
    observer: 'Dr. Smith Observatory',
    telescope: 'Schmidt-Cassegrain 14"',
    description: 'Follow-up observation of Fermi GBM trigger. Initial afterglow detected in R-band.'
  },
  {
    id: '2',
    imageUrl: 'https://placehold.co/400x300/764ba2/white?text=GRB+240814B',
    date: '2024-08-14',
    time: '03:15:22 UTC',
    gcnEvent: {
      triggerNumber: '240814B',
      ra: 256.78,
      dec: 45.32,
      error: 2.8,
      intensity: 6.2
    },
    observer: 'Amateur Astronomy Network',
    telescope: 'Newtonian 10"',
    description: 'Optical transient confirmed. Multiple exposures in V and R bands.'
  },
  {
    id: '3',
    imageUrl: 'https://placehold.co/400x300/667eea/white?text=GRB+240813C',
    date: '2024-08-13',
    time: '19:47:11 UTC',
    gcnEvent: {
      triggerNumber: '240813C',
      ra: 89.12,
      dec: -12.45,
      error: 4.1,
      intensity: 3.8
    },
    telescope: 'Refractor 6"',
    description: 'Late-time observation, no visible afterglow detected. Upper limit magnitude R > 19.5'
  }
])

const isLoading = ref(false)
</script>

<template>
  <div class="observation-list">
    <div class="container">
      <h2 class="section-title">Recent GRB Observations</h2>
      <p class="section-subtitle">
        Amateur astronomer observations of Gamma Ray Burst events detected by the Fermi Satellite
      </p>

      <div v-if="isLoading" class="loading">
        <div class="spinner"></div>
        <p>Loading observations...</p>
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

.cards-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 1.5rem;
  }
}
</style>
