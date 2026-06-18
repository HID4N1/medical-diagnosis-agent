import { useEffect } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import Loader from '../components/Loader'
import ProgressStepper from '../components/ProgressStepper'
import ReportCard from '../components/ReportCard'
import { useConsultation } from '../context/useConsultation'

export default function FinalReport() {
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

  return (
    <main className="app-shell">
      <ProgressStepper currentStep={4} />
      <section className="page-heading compact">
        <h1>Rapport Final Structuré</h1>
        <p>Synthèse clinique préliminaire issue du workflow académique.</p>
      </section>

      <p className="disclaimer">Ce système ne remplace pas une consultation médicale.</p>

      {loading && <Loader />}
      {error && <p className="error-message">{error}</p>}
      <ReportCard report={finalReport} />

      <div className="actions">
        <button type="button" onClick={handleNewConsultation}>
          Nouvelle consultation
        </button>
      </div>
    </main>
  )
}
