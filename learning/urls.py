from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.ThemeListView.as_view(), name='theme_list'),

    # Полный тест по теме (ДОЛЖЕН БЫТЬ ПЕРВЫМ!)
    path('theme/<slug:slug>/full_test/',
         views.FullThemeTestView.as_view(),
         name='full_theme_test'),

    # Результат полного теста
    path('theme/<slug:slug>/full_result/',
         views.FullTestResultView.as_view(),
         name='full_test_result'),

    # Страница темы (должна быть после полного теста)
    path('theme/<slug:slug>/', views.ThemeDetailView.as_view(), name='theme_detail'),

    # Тест по подтеме
    path('theme/<slug:theme_slug>/<slug:subtheme_slug>/test/',
         views.SubThemeTestView.as_view(),
         name='subtheme_test'),

    # Результат теста по подтеме
    path('theme/<slug:theme_slug>/<slug:subtheme_slug>/result/',
         views.TestResultView.as_view(),
         name='test_result'),

    # Страница подтемы (ДОЛЖНА БЫТЬ ПОСЛЕДНЕЙ!)
    path('theme/<slug:theme_slug>/<slug:subtheme_slug>/',
         views.SubThemeDetailView.as_view(),
         name='subtheme_detail'),
    path('login/', TemplateView.as_view(
        template_name='learning/login.html'), name='login'),
    path('register/', TemplateView.as_view(
        template_name='learning/register.html'), name='register'),
    path('logout/', TemplateView.as_view(
        template_name='learning/logout.html'), name='logout'),
]
