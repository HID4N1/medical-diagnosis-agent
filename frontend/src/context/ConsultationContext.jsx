import {
  useCallback,
  useMemo,
  useState,
} from 'react'
import {
  getReport,
  resumeConsultation,
  startConsultation,
} from '../api/consultationApi'
import { ConsultationContext } from './consultationState'

function applyApiResponse(response, setters) {
  setters.setStatus(response.status)
  setters.setCurrentQuestion(response.question || '')
  setters.setReviewRequest(response.review_request || '')
  setters.setFinalReport(response.final_report || '')
}

export function ConsultationProvider({ children }) {
  const [threadId, setThreadId] = useState('')
  const [status, setStatus] = useState('')
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [patientCase, setPatientCase] = useState('')
  const [patientAnswers, setPatientAnswers] = useState([])
  const [reviewRequest, setReviewRequest] = useState('')
  const [finalReport, setFinalReport] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const setters = useMemo(
    () => ({
      setStatus,
      setCurrentQuestion,
      setReviewRequest,
      setFinalReport,
    }),
    [],
  )

  const start = useCallback(async (initialPatientCase) => {
    setLoading(true)
    setError('')

    try {
      const response = await startConsultation(initialPatientCase)
      setThreadId(response.thread_id)
      setPatientCase(initialPatientCase)
      setPatientAnswers([])
      applyApiResponse(response, setters)
      return response
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [setters])

  const submitPatientAnswer = useCallback(async (answer) => {
    setLoading(true)
    setError('')

    try {
      const response = await resumeConsultation({
        thread_id: threadId,
        answer,
      })
      setPatientAnswers((answers) => [...answers, answer])
      applyApiResponse(response, setters)
      return response
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [setters, threadId])

  const submitPhysicianTreatment = useCallback(async (treatment) => {
    setLoading(true)
    setError('')

    try {
      const response = await resumeConsultation({
        thread_id: threadId,
        physician_treatment: treatment,
      })
      applyApiResponse(response, setters)
      return response
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [setters, threadId])

  const fetchReport = useCallback(async () => {
    if (!threadId) {
      return null
    }

    setLoading(true)
    setError('')

    try {
      const response = await getReport(threadId)
      setStatus(response.status)
      setFinalReport(response.final_report || '')
      return response
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [threadId])

  const resetConsultation = useCallback(() => {
    setThreadId('')
    setStatus('')
    setCurrentQuestion('')
    setPatientCase('')
    setPatientAnswers([])
    setReviewRequest('')
    setFinalReport('')
    setLoading(false)
    setError('')
  }, [])

  const value = {
    threadId,
    status,
    currentQuestion,
    patientCase,
    patientAnswers,
    reviewRequest,
    finalReport,
    loading,
    error,
    start,
    submitPatientAnswer,
    submitPhysicianTreatment,
    fetchReport,
    resetConsultation,
  }

  return (
    <ConsultationContext.Provider value={value}>
      {children}
    </ConsultationContext.Provider>
  )
}
