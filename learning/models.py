from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Theme(models.Model):
    name = models.CharField(
        max_length=100, unique=True, verbose_name='Название')
    slug = models.SlugField(
        max_length=120, unique=True, blank=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Краткое описание')
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Иконка (emoji или CSS класс)',
        verbose_name='Иконка')
    order = models.PositiveBigIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'name',)
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('learning:theme_detail', kwargs={'slug': self.slug})


class SubTheme(models.Model):
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        related_name='subthemes',
        verbose_name='Тема'
    )
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=120, blank=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Краткое описание')

    # Основной контент (статья с кодом)
    content = models.TextField(verbose_name='Статья (Markdown)')

    order = models.PositiveBigIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'name',)
        unique_together = ('theme', 'slug',)
        verbose_name = 'Подтема'
        verbose_name_plural = 'Подтемы'

    def __str__(self):
        return f'{self.theme.name} → {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('learning:subtheme_detail', kwargs={
            'theme_slug': self.theme.slug,
            'subtheme_slug': self.slug
        })


class Question(models.Model):
    subtheme = models.ForeignKey(
        SubTheme,
        on_delete=models.CASCADE,
        related_name='question',
        verbose_name='Подтема'
    )
    text = models.TextField(verbose_name='Текст вопроса')
    explanation = models.TextField(
        blank=True,
        verbose_name='Пояснение к ответу',
        help_text='Показывается после прохождения теста'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.subtheme.name} → Вопрос #{self.id}'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    text = models.CharField(max_length=500, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return f"{'✓' if self.is_correct else '○'} {self.text[:50]}"
