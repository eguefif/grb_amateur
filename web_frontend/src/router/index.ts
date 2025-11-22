import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import SubmitObservation from '@/views/SubmitObservation.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/submit-observation',
      name: 'submit-observation',
      component: SubmitObservation,
    },
  ],
})

export default router
