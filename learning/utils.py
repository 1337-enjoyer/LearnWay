from .models import Answer


def calculate_test_result(questions, user_answers):
    """
    Универсальная функция подсчета результатов теста.

    Args:
        questions: QuerySet или список вопросов
        user_answers: Словарь вида {question_id: answer_id}

    Returns:
        dict: {
            'correct': int,
            'total': int,
            'percent': int,
            'details': list  # детали по каждому вопросу
        }
    """
    correct = 0
    total = questions.count() if hasattr(questions, 'count') else len(questions)
    details = []

    for question in questions:
        user_answer_id = user_answers.get(str(question.id))
        user_answer = None
        correct_answer = None
        is_correct = False

        # Находим правильный ответ
        for answer in question.answers.all():
            if answer.is_correct:
                correct_answer = answer
                break

        # Находим ответ пользователя
        if user_answer_id:
            user_answer = Answer.objects.filter(
                id=user_answer_id, question=question
            ).first()
            if user_answer and user_answer.is_correct:
                is_correct = True
                correct += 1

        details.append({
            'question_id': question.id,
            'question_text': question.text,
            'question_explanation': question.explanation,
            'user_answer_id': user_answer_id,
            'user_answer_text': user_answer.text if user_answer else None,
            'is_correct': is_correct,
            'correct_answer_text': correct_answer.text if correct_answer else None,
        })

    percent = int((correct / total) * 100) if total > 0 else 0

    return {
        'correct': correct,
        'total': total,
        'percent': percent,
        'details': details,
    }
