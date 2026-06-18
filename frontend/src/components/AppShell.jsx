export default function AppShell({ children }) {
  return (
    <div className="app-frame">
      <header className="app-header">
        <div className="brand-block" aria-label="MediGraph">
          <div>
            <p className="brand-name">MediGraph</p>
            <p className="brand-subtitle">Orientation clinique préliminaire</p>
          </div>
        </div>
        <span className="academic-badge">Projet académique</span>
      </header>

      <main className="app-shell">{children}</main>

      <footer className="app-footer">
        Ce système ne remplace pas une consultation médicale.
      </footer>
    </div>
  )
}
