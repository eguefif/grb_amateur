<script setup lang="ts">
import EmailRegistration from './EmailRegistration.vue'
</script>

<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <div class="logo">
          <div class="logo-icon">⚡</div>
          <h1 class="logo-text">Gamma Ray Burst</h1>
        </div>

        <EmailRegistration />
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: linear-gradient(180deg, #0a0e27 0%, #16213e 50%, #1a1a2e 100%);
  color: white;
  box-shadow: 0 4px 20px rgba(138, 43, 226, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 2px solid rgba(138, 43, 226, 0.3);
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(2px 2px at 20% 30%, white, transparent),
    radial-gradient(2px 2px at 60% 70%, rgba(138, 43, 226, 0.8), transparent),
    radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(1px 1px at 80% 10%, rgba(138, 43, 226, 0.6), transparent),
    radial-gradient(2px 2px at 90% 60%, white, transparent),
    radial-gradient(1px 1px at 33% 85%, white, transparent),
    radial-gradient(1px 1px at 15% 75%, rgba(138, 43, 226, 0.7), transparent);
  background-size: 200% 200%;
  background-position: 0% 0%;
  opacity: 0.5;
  animation: twinkle 8s ease-in-out infinite;
  pointer-events: none;
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.25rem 1rem;
  position: relative;
  z-index: 1;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 10px rgba(138, 43, 226, 0.8));
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    filter: drop-shadow(0 0 10px rgba(138, 43, 226, 0.8));
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
    filter: drop-shadow(0 0 20px rgba(138, 43, 226, 1));
  }
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(138, 43, 226, 0.5);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .logo {
    justify-content: center;
  }

  .logo-text {
    font-size: 1.25rem;
  }
}
</style>
