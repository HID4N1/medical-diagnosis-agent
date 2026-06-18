import { Route, Routes } from 'react-router-dom'
import FinalReport from '../pages/FinalReport'
import PatientQuestions from '../pages/PatientQuestions'
import PhysicianReview from '../pages/PhysicianReview'
import StartConsultation from '../pages/StartConsultation'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<StartConsultation />} />
      <Route path="/questions" element={<PatientQuestions />} />
      <Route path="/physician" element={<PhysicianReview />} />
      <Route path="/report" element={<FinalReport />} />
    </Routes>
  )
}
