import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import AppShell from '../components/AppShell'
import Loader from '../components/Loader'
import ProgressStepper from '../components/ProgressStepper'
import ReportCard from '../components/ReportCard'
import { useConsultation } from '../context/useConsultation'

export default function PhysicianReview() {
  const [treatment, setTreatment] = useState('')
  const navigate = useNavigate()
  const {
    error,
    loading,
    reviewRequest,
    submitPhysicianTreatment,
    threadId,
  } = useConsultation()

  if (!threadId) {
    return <Navigate to="/" replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedTreatment = treatment.trim()
    if (!trimmedTreatment) {
      return
    }

    try {
      const response = await submitPhysicianTreatment(trimmedTreatment)
      if (response.status === 'completed') {
        navigate('/report')
      }
    } catch {
      // The context exposes the user-facing error message.
    }
  }

  return (
    <AppShell>
      <ProgressStepper currentStep={3} />
      <section className="page-heading">
        <h1>Revue médicale</h1>
        <p>
          Validation humaine requise avant génération du rapport final.
        </p>
      </section>

      <p className="warning-note">
        Le rapport final sera généré uniquement après cette étape de validation
        humaine.
      </p>

      <section className="review-layout">
        <div>
          <p className="section-label">Synthèse transmise au médecin</p>
          <ReportCard report={reviewRequest} />
        </div>

        <form className="card form-card sticky-card" onSubmit={handleSubmit}>
          <label htmlFor="physician-treatment">
            Conduite à tenir proposée
          </label>
          <textarea
            id="physician-treatment"
            placeholder="Repos, hydratation, surveillance clinique et consultation rapide en cas d’aggravation."
            value={treatment}
            onChange={(event) => setTreatment(event.target.value)}
            rows={8}
          />
          {error && <p className="error-message">{error}</p>}
          {loading ? (
            <Loader />
          ) : (
              <button type="submit" disabled={!treatment.trim()}>
              Valider la revue
            </button>
          )}
        </form>
      </section>
    </AppShell>
  )
}
