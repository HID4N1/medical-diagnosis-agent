import { useContext } from 'react'
import { ConsultationContext } from './consultationState'

export function useConsultation() {
  const context = useContext(ConsultationContext)
  if (!context) {
    throw new Error('useConsultation must be used within ConsultationProvider')
  }

  return context
}
