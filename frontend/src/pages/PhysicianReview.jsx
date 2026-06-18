import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
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
    <main className="app-shell">
      <ProgressStepper currentStep={3} />
      <section className="page-heading compact">
        <h1>Revue du Médecin Traitant</h1>
        <p>Validation humaine de la recommandation intermédiaire.</p>
      </section>

      <p className="disclaimer">Ce système ne remplace pas une consultation médicale.</p>

      <ReportCard report={reviewRequest} />

      <form className="card form-card" onSubmit={handleSubmit}>
        <label htmlFor="physician-treatment">
          Conduite à tenir proposée par le médecin
        </label>
        <textarea
          id="physician-treatment"
          placeholder="Ajouter la conduite à tenir proposée par le médecin…"
          value={treatment}
          onChange={(event) => setTreatment(event.target.value)}
          rows={6}
        />
        {error && <p className="error-message">{error}</p>}
        {loading ? (
          <Loader />
        ) : (
          <button type="submit" disabled={!treatment.trim()}>
            Valider la revue médicale
          </button>
        )}
      </form>
    </main>
  )
}
