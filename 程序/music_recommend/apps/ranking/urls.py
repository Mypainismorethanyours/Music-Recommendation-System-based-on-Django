from django.urls import path

from . import views


urlpatterns = [
    path('ranking/', views.RankingView.as_view(), name='ranking'),
    path('predict',views.predict)
]