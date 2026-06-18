import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import AppShell from '../components/AppShell'
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
    <AppShell>
      <ProgressStepper currentStep={2} />
      <section className="page-heading">
        <h1>Entretien patient</h1>
        <p>
          Le système collecte cinq réponses pour enrichir l’état partagé du
          graphe.
        </p>
      </section>

      <section className="content-grid">
        <div className="workflow-column">
          <QuestionCard question={currentQuestion} questionNumber={questionNumber} />

          <form className="card form-card" onSubmit={handleSubmit}>
            <div className="form-title-row">
              <label htmlFor="patient-answer">Réponse du patient</label>
            </div>
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
                Enregistrer la réponse
              </button>
            )}
          </form>
        </div>

        <aside className="card info-card">
          <h2>État du workflow</h2>
          <dl className="workflow-state">
            <div>
              <dt>Réponses collectées</dt>
              <dd>{patientAnswers.length}/5</dd>
            </div>
            <div>
              <dt>Étape actuelle</dt>
              <dd>Diagnostic Agent</dd>
            </div>
          </dl>
        </aside>
      </section>
    </AppShell>
  )
}
