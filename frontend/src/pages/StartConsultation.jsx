import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AppShell from '../components/AppShell'
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
    <AppShell>
      <ProgressStepper currentStep={1} />

      <section className="hero-card card">
        <div className="hero-copy">
          <h1>Système d’orientation clinique</h1>
          <p>
            Workflow multi-agents pour la collecte des informations patient,
            la synthèse préliminaire et la revue médicale.
          </p>

          <div className="meta-list" aria-label="Technologies principales">
            <span>LangGraph</span>
            <span>FastAPI</span>
            <span>MCP</span>
            <span>Human-in-the-Loop</span>
          </div>

          <p className="disclaimer">
            Projet académique — ne fournit pas de diagnostic définitif.
          </p>
        </div>

        <form className="form-panel" onSubmit={handleSubmit}>
          <h2>Nouveau cas patient</h2>
          <label htmlFor="patient-case">Description initiale du cas</label>
          <textarea
            id="patient-case"
            placeholder="Patient avec toux légère, fatigue et fièvre modérée depuis deux jours."
            value={caseText}
            onChange={(event) => setCaseText(event.target.value)}
            rows={9}
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
      </section>
    </AppShell>
  )
}
