export default function QuestionCard({ question, questionNumber }) {
  return (
    <section className="card question-card">
      <div className="question-card-header">
        <p className="card-title">Question {questionNumber} sur 5</p>
      </div>
      <h2>{question || 'Question en cours de préparation...'}</h2>
    </section>
  )
}
