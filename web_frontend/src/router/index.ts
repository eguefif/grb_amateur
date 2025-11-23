import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import SubmitObservation from '@/views/SubmitObservation.vue'
import EventDetail from '@/views/EventDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home-page',
      component: HomePage,
    },
    {
      path: '/submit-observation',
      name: 'submit-observation',
      component: SubmitObservation,
    },
    {
      path: '/event/:id',
      name: 'event-detail',
      component: EventDetail,
    },
  ],
})

export default router
