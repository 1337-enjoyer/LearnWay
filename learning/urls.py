from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.ThemeListView.as_view(), name='theme_list'),
    path('theme/<slug:slug>/full_test/',
         views.FullThemeTestView.as_view(), name='full_theme_test'),
    path('theme/<slug:slug>/full_result/',
         views.FullTestResultView.as_view(), name='full_test_result'),
    path('theme/<slug:slug>/<slug:subtheme_slug>/',
         views.ThemeDetailView.as_view(),
         name='theme_detail_with_subtheme'),
    path('theme/<slug:slug>/', views.ThemeDetailView.as_view(), name='theme_detail'),
    path('theme/<slug:theme_slug>/<slug:subtheme_slug>/test/',
         views.SubThemeTestView.as_view(),
         name='subtheme_test'),
    path('theme/<slug:theme_slug>/<slug:subtheme_slug>/result/',
         views.TestResultView.as_view(),
         name='test_result'),
]
