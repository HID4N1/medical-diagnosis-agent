export default function QuestionCard({ question, questionNumber }) {
  return (
    <section className="card question-card">
      <p className="eyebrow">Question {questionNumber} sur 5</p>
      <h2>{question}</h2>
    </section>
  )
}
