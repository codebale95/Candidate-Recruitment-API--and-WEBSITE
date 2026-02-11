from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.candidate_list, name='candidate_list'),
    path('<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('create/', views.candidate_create, name='candidate_create'),
    path('<int:pk>/update/', views.candidate_update, name='candidate_update'),
    path('<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    path('<int:pk>/move/', views.move_stage, name='move_stage'),
]
