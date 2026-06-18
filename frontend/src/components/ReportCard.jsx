export default function ReportCard({ report }) {
  return (
    <article className="card report-card">
      <pre>{report || 'Rapport non disponible pour le moment.'}</pre>
    </article>
  )
}
