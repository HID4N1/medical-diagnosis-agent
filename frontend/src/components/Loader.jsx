export default function Loader() {
  return (
    <div className="loader" role="status" aria-live="polite">
      <span className="loader-dot" aria-hidden="true"></span>
      Traitement en cours…
    </div>
  )
}
