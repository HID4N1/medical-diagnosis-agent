import { useEffect, useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import AppShell from '../components/AppShell'
import Loader from '../components/Loader'
import ProgressStepper from '../components/ProgressStepper'
import ReportCard from '../components/ReportCard'
import { useConsultation } from '../context/useConsultation'

export default function FinalReport() {
  const [copyStatus, setCopyStatus] = useState('')
  const navigate = useNavigate()
  const {
    error,
    fetchReport,
    finalReport,
    loading,
    resetConsultation,
    threadId,
  } = useConsultation()

  useEffect(() => {
    if (threadId && !finalReport) {
      fetchReport()
    }
  }, [fetchReport, finalReport, threadId])

  if (!threadId) {
    return <Navigate to="/" replace />
  }

  function handleNewConsultation() {
    resetConsultation()
    navigate('/')
  }

  async function handleCopyReport() {
    if (!finalReport || !navigator.clipboard) {
      return
    }

    await navigator.clipboard.writeText(finalReport)
    setCopyStatus('Rapport copié')
    window.setTimeout(() => setCopyStatus(''), 1800)
  }

  return (
    <AppShell>
      <ProgressStepper currentStep={4} />
      <section className="page-heading report-heading">
        <div>
          <h1>Rapport final</h1>
          <p>Rapport structuré généré après revue humaine.</p>
        </div>
        <span className="success-badge">Consultation terminée</span>
      </section>

      {loading && <Loader />}
      {error && <p className="error-message">{error}</p>}
      <ReportCard report={finalReport} />

      <div className="actions">
        <button
          className="secondary-button"
          type="button"
          onClick={handleCopyReport}
          disabled={!finalReport}
        >
          Copier le rapport
        </button>
        <button type="button" onClick={handleNewConsultation}>
          Nouvelle consultation
        </button>
      </div>
      {copyStatus && <p className="copy-status">{copyStatus}</p>}
    </AppShell>
  )
}
