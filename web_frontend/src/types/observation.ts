export interface GrbObservation {
  id: number
  coordinates: string
  coordinate_sytem: string
  instrument: string
  observed_time: string
  alert_id: number
  file_path?: string
}
