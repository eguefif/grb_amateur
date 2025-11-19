export interface GrbObservation {
  id: string
  imageUrl: string
  date: string
  time: string
  gcnEvent: {
    triggerNumber: string
    ra: number
    dec: number
    error: number
    intensity: number
  }
  observer?: string
  telescope?: string
  description?: string
}
