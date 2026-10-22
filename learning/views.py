import random

from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count

from .models import Theme, SubTheme, Question
from .forms import TestForm
from .utils import calculate_test_result


class ThemeListView(ListView):
    model = Theme
    template_name = 'learning/theme_list.html'
    context_object_name = 'themes'

    def get_queryset(self):
        return Theme.objects.annotate(
            subtheme_count=Count('subthemes')
        )


class ThemeDetailView(DetailView):
    model = Theme
    template_name = 'learning/theme_detail.html'
    context_object_name = 'theme'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subtheme_slug = self.kwargs.get('subtheme_slug')
        if subtheme_slug:
            current_subtheme = get_object_or_404(
                SubTheme,
                theme=self.object,
                slug=subtheme_slug
            )
        else:
            current_subtheme = self.object.subthemes.order_by('order').first()

        context['current_subtheme'] = current_subtheme
        return context


class SubThemeDetailView(DetailView):
    model = SubTheme

    def get(self, request, *args, **kwargs):
        subtheme = self.get_object()
        return redirect('learning:theme_detail_with_subtheme',
                        slug=subtheme.theme.slug,
                        subtheme_slug=subtheme.slug)


class SubThemeTestView(FormView):
    """Тест по конкретной подтеме"""
    template_name = 'learning/subtheme_test.html'
    form_class = TestForm

    def dispatch(self, request, *args, **kwargs):
        self.theme = get_object_or_404(Theme, slug=self.kwargs['theme_slug'])
        self.subtheme = get_object_or_404(
            SubTheme, theme=self.theme, slug=self.kwargs['subtheme_slug']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        questions = list(self.subtheme.questions.all())
        random.shuffle(questions)
        kwargs['questions'] = questions
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtheme'] = self.subtheme
        questions = list(self.subtheme.questions.all())
        random.shuffle(questions)
        for question in questions:
            question.shuffled_answers = question.get_shuffled_answers()

        context['questions'] = questions
        return context

    def form_valid(self, form):
        user_answers = form.cleaned_data.get('answers', {})
        questions = self.subtheme.questions.all()

        result = calculate_test_result(questions, user_answers)

        self.request.session['test_result'] = {
            'correct': result['correct'],
            'total': result['total'],
            'percent': result['percent'],
            'subtheme_id': self.subtheme.id,
            'answers': user_answers,
            'details': result['details'],
        }

        return redirect('learning:test_result',
                        theme_slug=self.theme.slug,
                        subtheme_slug=self.subtheme.slug)


class FullThemeTestView(FormView):
    """Полный тест по всей теме (все подтемы)"""
    template_name = 'learning/full_theme_test.html'
    form_class = TestForm

    def dispatch(self, request, *args, **kwargs):
        self.theme = get_object_or_404(Theme, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        questions = list(Question.objects.filter(subtheme__theme=self.theme))
        random.shuffle(questions)
        kwargs['questions'] = questions
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theme'] = self.theme

        questions = list(Question.objects.filter(subtheme__theme=self.theme))
        random.shuffle(questions)
        for question in questions:
            question.shuffled_answers = question.get_shuffled_answers()

        context['questions'] = questions
        return context

    def form_valid(self, form):
        user_answers = form.cleaned_data.get('answers', {})
        questions = Question.objects.filter(subtheme__theme=self.theme)

        result = calculate_test_result(questions, user_answers)

        self.request.session['test_result'] = {
            'correct': result['correct'],
            'total': result['total'],
            'percent': result['percent'],
            'theme_id': self.theme.id,
            'answers': user_answers,
            'details': result['details'],
        }

        return redirect('learning:full_test_result', slug=self.theme.slug)


class TestResultView(TemplateView):
    template_name = 'learning/test_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = get_object_or_404(Theme, slug=self.kwargs['theme_slug'])
        subtheme = get_object_or_404(
            SubTheme, theme=theme, slug=self.kwargs['subtheme_slug'])

        result = self.request.session.get('test_result', {})

        context['subtheme'] = subtheme
        context['correct_answers'] = result.get('correct', 0)
        context['total_questions'] = result.get('total', 0)
        context['score_percent'] = result.get('percent', 0)
        context['details'] = result.get('details', [])
        context['answers'] = result.get('answers', {})

        return context


class FullTestResultView(TemplateView):
    """Результат полного теста по теме"""
    template_name = 'learning/full_test_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme = get_object_or_404(Theme, slug=self.kwargs['slug'])
        result = self.request.session.get('test_result', {})
        context['theme'] = theme
        context['correct_answers'] = result.get('correct', 0)
        context['total_questions'] = result.get('total', 0)
        context['score_percent'] = result.get('percent', 0)
        context['details'] = result.get('details', [])
        return context
