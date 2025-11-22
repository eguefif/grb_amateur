import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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

export const useEventsStore = defineStore('events', () => {
  const events = ref<GRBEvent[]>([])

  const setEvents = (newEvents: GRBEvent[]) => {
    events.value = newEvents
  }

  const getEventById = computed(() => {
    return (id: number): GRBEvent | undefined => {
      return events.value.find(event => event.id === id)
    }
  })

  return {
    events,
    setEvents,
    getEventById
  }
})
