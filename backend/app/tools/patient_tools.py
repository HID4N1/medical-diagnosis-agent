QUESTIONS = {
    1: "Depuis quand présentez-vous ces symptômes ?",
    2: "Avez-vous de la fièvre ou des frissons ?",
    3: "Évaluez votre douleur ou votre inconfort sur une échelle de 0 à 10.",
    4: "Avez-vous des antécédents médicaux importants ?",
    5: "Prenez-vous actuellement un traitement ou un médicament ?",
}


def ask_patient(question_number: int, patient_case: str) -> str:
    return QUESTIONS[question_number]
