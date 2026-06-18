import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Loader from '../components/Loader'
import ProgressStepper from '../components/ProgressStepper'
import { useConsultation } from '../context/useConsultation'

export default function StartConsultation() {
  const [caseText, setCaseText] = useState('')
  const navigate = useNavigate()
  const { error, loading, start } = useConsultation()

  function routeFromStatus(status) {
    if (status === 'waiting_patient') {
      navigate('/questions')
    } else if (status === 'waiting_physician') {
      navigate('/physician')
    } else if (status === 'completed') {
      navigate('/report')
    }
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const trimmedCase = caseText.trim()
    if (!trimmedCase) {
      return
    }

    try {
      const response = await start(trimmedCase)
      routeFromStatus(response.status)
    } catch {
      // The context exposes the user-facing error message.
    }
  }

  return (
    <main className="app-shell">
      <ProgressStepper currentStep={1} />

      <section className="page-heading">
        <h1>Système Multi-Agents d’Orientation Clinique Préliminaire</h1>
        <p>Projet académique basé sur LangGraph, FastAPI et MCP</p>
      </section>

      <p className="disclaimer">Ce système ne remplace pas une consultation médicale.</p>

      <form className="card form-card" onSubmit={handleSubmit}>
        <label htmlFor="patient-case">Cas initial du patient</label>
        <textarea
          id="patient-case"
          placeholder="Décrivez le cas initial du patient…"
          value={caseText}
          onChange={(event) => setCaseText(event.target.value)}
          rows={8}
        />
        {error && <p className="error-message">{error}</p>}
        {loading ? (
          <Loader />
        ) : (
          <button type="submit" disabled={!caseText.trim()}>
            Démarrer la consultation
          </button>
        )}
      </form>
    </main>
  )
}
