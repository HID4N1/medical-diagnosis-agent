import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import Loader from '../components/Loader'
import ProgressStepper from '../components/ProgressStepper'
import QuestionCard from '../components/QuestionCard'
import { useConsultation } from '../context/useConsultation'

export default function PatientQuestions() {
  const [answer, setAnswer] = useState('')
  const navigate = useNavigate()
  const {
    currentQuestion,
    error,
    loading,
    patientAnswers,
    submitPatientAnswer,
    threadId,
  } = useConsultation()

  if (!threadId) {
    return <Navigate to="/" replace />
  }

  function routeFromStatus(status) {
    if (status === 'waiting_physician') {
      navigate('/physician')
    } else if (status === 'completed') {
      navigate('/report')
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedAnswer = answer.trim()
    if (!trimmedAnswer) {
      return
    }

    try {
      const response = await submitPatientAnswer(trimmedAnswer)
      setAnswer('')
      routeFromStatus(response.status)
    } catch {
      // The context exposes the user-facing error message.
    }
  }

  const questionNumber = Math.min(patientAnswers.length + 1, 5)

  return (
    <main className="app-shell">
      <ProgressStepper currentStep={2} />
      <section className="page-heading compact">
        <h1>Questions Patient</h1>
        <p>Orientation clinique préliminaire : {questionNumber} / 5</p>
      </section>

      <p className="disclaimer">Ce système ne remplace pas une consultation médicale.</p>

      <QuestionCard question={currentQuestion} questionNumber={questionNumber} />

      <form className="card form-card" onSubmit={handleSubmit}>
        <label htmlFor="patient-answer">Réponse du patient</label>
        <textarea
          id="patient-answer"
          placeholder="Réponse du patient…"
          value={answer}
          onChange={(event) => setAnswer(event.target.value)}
          rows={6}
        />
        {error && <p className="error-message">{error}</p>}
        {loading ? (
          <Loader />
        ) : (
          <button type="submit" disabled={!answer.trim()}>
            Envoyer la réponse
          </button>
        )}
      </form>
    </main>
  )
}
