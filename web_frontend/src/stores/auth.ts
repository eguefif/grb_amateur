import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const userEmail = ref<string | null>(localStorage.getItem('user_email'))

  const isAuthenticated = computed(() => !!accessToken.value)

  const setAuth = (token: string, email: string) => {
    accessToken.value = token
    userEmail.value = email
    localStorage.setItem('access_token', token)
    localStorage.setItem('user_email', email)
  }

  const logout = () => {
    accessToken.value = null
    userEmail.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_email')
  }

  const getAuthHeader = () => {
    if (accessToken.value) {
      return {
        Authorization: `Bearer ${accessToken.value}`
      }
    }
    return {}
  }

  return {
    accessToken,
    userEmail,
    isAuthenticated,
    setAuth,
    logout,
    getAuthHeader
  }
})
