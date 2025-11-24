<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const handleGoHome = () => {
  router.push({ name: 'home-page' })
}
</script>

<template>
  <div class="email-confirmed-page">
    <div class="confirmation-container">
      <div class="confirmation-card">
        <div class="icon-wrapper">
          <svg
            class="check-icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>

        <h1 class="title">Email Confirmed!</h1>
        <p class="message">
          Your email address has been successfully verified. You're all set to receive GRB alerts and submit observations.
        </p>

        <button @click="handleGoHome" class="btn-home">
          Go to Homepage
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.email-confirmed-page {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  background: linear-gradient(180deg, #0a0e27 0%, #16213e 50%, #1a1a2e 100%);
  min-height: calc(100vh - 100px);
}

.confirmation-container {
  width: 100%;
  max-width: 480px;
}

.confirmation-card {
  background: rgba(26, 26, 46, 0.9);
  border-radius: 16px;
  padding: 3rem 2.5rem;
  box-shadow: 0 8px 32px rgba(138, 43, 226, 0.3);
  border: 1px solid rgba(138, 43, 226, 0.2);
  text-align: center;
}

.icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.check-icon {
  width: 80px;
  height: 80px;
  color: #10b981;
  animation: checkmark 0.6s ease-in-out;
}

@keyframes checkmark {
  0% {
    transform: scale(0) rotate(-45deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotate(5deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #fff 0%, #b19cd9 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.message {
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 2rem 0;
  font-size: 1.05rem;
  line-height: 1.6;
}

.btn-home {
  padding: 0.875rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  outline: none;
  background: linear-gradient(135deg, #8a2be2 0%, #5a189a 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
  min-width: 200px;
}

.btn-home:hover {
  background: linear-gradient(135deg, #9d4edd 0%, #6b1fb1 100%);
  box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
  transform: translateY(-2px);
}

.btn-home:active {
  transform: translateY(0);
}

@media (max-width: 480px) {
  .confirmation-card {
    padding: 2.5rem 1.5rem;
  }

  .title {
    font-size: 1.75rem;
  }

  .check-icon {
    width: 64px;
    height: 64px;
  }

  .message {
    font-size: 1rem;
  }
}
</style>
