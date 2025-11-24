import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import SubmitObservation from '@/views/SubmitObservation.vue'
import EventDetail from '@/views/EventDetail.vue'
import SignUp from '@/views/SignUp.vue'
import SignIn from '@/views/SignIn.vue'
import EmailConfirmed from '@/views/EmailConfirmed.vue'

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
    {
      path: '/sign-up',
      name: 'sign-up',
      component: SignUp,
    },
    {
      path: '/sign-in',
      name: 'sign-in',
      component: SignIn,
    },
    {
      path: '/email-confirmed',
      name: 'email-confirmed',
      component: EmailConfirmed,
    },
  ],
})

export default router
