from .models import Answer


def calculate_test_result(questions, user_answers):
    correct = 0
    total = (
        questions.count()
        if hasattr(questions, 'count')
        else len(questions)
    )
    details = []

    for question in questions:
        user_answer_id = user_answers.get(str(question.id))
        is_correct = False

        if user_answer_id:
            answer = Answer.objects.filter(
                id=user_answer_id, question=question).first()
            if answer and answer.is_correct:
                is_correct = True
                correct += 1

        details.append({
            'question_id': question.id,
            'user_answer_id': user_answer_id,
            'is_correct': is_correct,
        })

    percent = int((correct / total) * 100) if total > 0 else 0

    return {
        'correct': correct,
        'total': total,
        'percent': percent,
        'details': details,
    }
