import axios from 'axios'
import type { GrbObservation } from '@/types/observation'

const api = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getObservations = async (offset = 0, limit = 5): Promise<GrbObservation[]> => {
  const response = await api.get<GrbObservation[]>('/observations/', {
    params: {
      offset,
      limit,
    },
  })
  return response.data
}

export default api
