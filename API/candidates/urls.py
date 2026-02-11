from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'candidates', views.CandidateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Web views
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('candidates/', views.CandidateListView.as_view(), name='candidate_list'),
    path('candidates/<int:pk>/', views.CandidateDetailView.as_view(), name='candidate_detail'),
    path('candidates/create/', views.CandidateCreateView.as_view(), name='candidate_create'),
    path('candidates/<int:pk>/update/', views.CandidateUpdateView.as_view(), name='candidate_update'),
    path('candidates/<int:pk>/move/', views.move_to_next_stage_view, name='move_to_next_stage'),
    path('candidates/<int:pk>/reject/', views.reject_candidate_view, name='reject_candidate'),
]
