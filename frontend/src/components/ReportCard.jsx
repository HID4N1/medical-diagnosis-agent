export default function ReportCard({ report }) {
  const lines = (report || 'Rapport non disponible pour le moment.').split('\n')

  return (
    <article className="card report-card">
      <div className="report-content">
        {lines.map((line, index) => {
          const isDisclaimer = line.includes(
            'Ce système ne remplace pas une consultation médicale.',
          )
          const isSectionTitle = line && lines[index + 1]?.startsWith('---')
          const isRule = line.startsWith('---')

          return (
            <p
              className={[
                'report-line',
                isDisclaimer ? 'disclaimer-line' : '',
                isSectionTitle ? 'report-section-title' : '',
                isRule ? 'report-rule' : '',
              ].filter(Boolean).join(' ')}
              key={`${line}-${index}`}
            >
              {line || '\u00A0'}
            </p>
          )
        })}
      </div>
    </article>
  )
}
