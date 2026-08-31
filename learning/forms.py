from django import forms


class TestForm(forms.Form):
    """Форма для прохождения теста"""
    
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        for question in questions:
            field_name = f'question_{question.id}'
            self.fields[field_name] = forms.ChoiceField(
                label=question.text,
                choices=[('', 'Выберите ответ...')] + [
                    (answer.id, answer.text) for answer in question.answers.all()
                ],
                widget=forms.RadioSelect,
                required=True,
            )
    
    def clean(self):
        cleaned_data = super().clean()
        # Собираем все ответы в один словарь
        answers = {}
        for field_name, value in cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = field_name.split('_')[1]
                answers[question_id] = value
        cleaned_data['answers'] = answers
        return cleaned_data