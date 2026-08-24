import nested_admin  # ← ИМПОРТ!
from django.contrib import admin
from .models import Theme, SubTheme, Question, Answer


class AnswerInline(nested_admin.NestedTabularInline):  # ← NestedTabularInline
    model = Answer
    extra = 4
    fields = ['text', 'is_correct']
    can_delete = True


class QuestionInline(nested_admin.NestedTabularInline):  # ← NestedTabularInline
    model = Question
    extra = 1
    fields = ['text', 'explanation', 'order']
    inlines = [AnswerInline]  # ← ТЕПЕРЬ РАБОТАЕТ!
    show_change_link = True


class SubThemeInline(nested_admin.NestedTabularInline):  # ← NestedTabularInline
    model = SubTheme
    extra = 1
    fields = ['name', 'slug', 'description', 'content', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [QuestionInline]  # ← ТЕПЕРЬ РАБОТАЕТ!
    show_change_link = True


@admin.register(Theme)
class ThemeAdmin(nested_admin.NestedModelAdmin):  # ← NestedModelAdmin
    list_display = ['name', 'slug', 'icon', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubThemeInline]
    fields = ['name', 'slug', 'icon', 'description', 'order']


@admin.register(SubTheme)
class SubThemeAdmin(nested_admin.NestedModelAdmin):  # ← NestedModelAdmin
    list_display = ['name', 'theme', 'order', 'created_at']
    list_filter = ['theme']
    search_fields = ['name', 'content']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [QuestionInline]
    fields = ['theme', 'name', 'slug', 'description', 'content', 'order']


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):  # ← NestedModelAdmin
    list_display = ['id', 'subtheme', 'text_preview', 'order', 'answers_count']
    list_filter = ['subtheme__theme', 'subtheme']
    search_fields = ['text']
    inlines = [AnswerInline]
    fields = ['subtheme', 'text', 'explanation', 'order']

    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = "Текст вопроса"

    def answers_count(self, obj):
        return obj.answers.count()
    answers_count.short_description = "Кол-во ответов"


@admin.register(Answer)
class AnswerAdmin(nested_admin.NestedModelAdmin):  # ← NestedModelAdmin
    list_display = ['text_preview', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__subtheme__theme']
    search_fields = ['text']
    fields = ['question', 'text', 'is_correct']

    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = "Текст ответа"
