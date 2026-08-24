from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class LearningUser(AbstractUser):
    bio = models.TextField(blank=True, verbose_name='О себе')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    telegram = models.CharField(
        max_length=100, blank=True, verbose_name='Telegram')
    github = models.CharField(
        max_length=100, blank=True, verbose_name='GitHub')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class UserProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Пользователь'
    )
    subtheme = models.ForeignKey(
        'learning.SubTheme',
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name='Подтема'
    )
    best_score = models.PositiveIntegerField(
        default=0,
        verbose_name='"Лучший результат (%)',
        help_text='Процент правильных ответов'
    )
    attempts = models.PositiveIntegerField(
        default=0, verbose_name='Количество попыток')
    last_attempt = models.DateTimeField(
        auto_now=True, verbose_name='Последняя попытка')

    class Meta:
        unique_together = ['user', 'subtheme']
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"
        ordering = ['-last_attempt']

    def __str__(self):
        return f"{self.user.username} - {self.subtheme.name}: {self.best_score}%"

    def update_score(self, new_score):
        if new_score > self.best_score:
            self.best_score = new_score
        self.attempts += 1
        self.save()
