import { ConsultationProvider } from './context/ConsultationContext'
import AppRoutes from './routes/AppRoutes'

export default function App() {
  return (
    <ConsultationProvider>
      <AppRoutes />
    </ConsultationProvider>
  )
}
