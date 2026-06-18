import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

function normalizeError(error) {
  const detail = error.response?.data?.detail
  if (detail) {
    return Array.isArray(detail) ? detail.map((item) => item.msg).join(' ') : detail
  }

  return error.message || 'Une erreur est survenue.'
}

export async function startConsultation(patientCase) {
  try {
    const response = await apiClient.post('/consultation/start', {
      patient_case: patientCase,
    })
    return response.data
  } catch (error) {
    throw new Error(normalizeError(error), { cause: error })
  }
}

export async function resumeConsultation(payload) {
  try {
    const response = await apiClient.post('/consultation/resume', payload)
    return response.data
  } catch (error) {
    throw new Error(normalizeError(error), { cause: error })
  }
}

export async function getConsultation(threadId) {
  try {
    const response = await apiClient.get(`/consultation/${threadId}`)
    return response.data
  } catch (error) {
    throw new Error(normalizeError(error), { cause: error })
  }
}

export async function getReport(threadId) {
  try {
    const response = await apiClient.get(`/consultation/${threadId}/report`)
    return response.data
  } catch (error) {
    throw new Error(normalizeError(error), { cause: error })
  }
}
