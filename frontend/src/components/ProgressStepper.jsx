const steps = [
  'Cas',
  'Questions',
  'Revue',
  'Rapport',
]

export default function ProgressStepper({ currentStep = 1 }) {
  return (
    <ol className="stepper" aria-label="Progression de la consultation">
      {steps.map((step, index) => {
        const stepNumber = index + 1
        const stateClass = stepNumber < currentStep ? 'done' : ''
        const activeClass = stepNumber === currentStep ? 'active' : ''

        return (
          <li
            className={`step ${stateClass} ${activeClass}`.trim()}
            key={step}
          >
            <span className="step-number" aria-hidden="true">
              {stepNumber < currentStep ? '✓' : stepNumber}
            </span>
            <span>{step}</span>
          </li>
        )
      })}
    </ol>
  )
}
