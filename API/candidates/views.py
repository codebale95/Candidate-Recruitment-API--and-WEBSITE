from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Candidate
from .serializers import CandidateSerializer
from .permissions import IsRecruiterOrReadOnly

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated, IsRecruiterOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            # Candidates can only see their own application
            return Candidate.objects.filter(email=user.email)
        return Candidate.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def move_to_next_stage(self, request, pk=None):
        candidate = get_object_or_404(Candidate, pk=pk)
        if request.user.role != 'recruiter':
            return Response({'error': 'Only recruiters can move candidates to next stage'}, status=status.HTTP_403_FORBIDDEN)

        stage_order = ['applied', 'screening', 'interview', 'hired']
        current_index = stage_order.index(candidate.stage)

        if current_index < len(stage_order) - 1:
            candidate.stage = stage_order[current_index + 1]
            candidate.save()
            serializer = self.get_serializer(candidate)
            return Response(serializer.data)
        else:
            return Response({'error': 'Candidate is already at the final stage'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        candidate = get_object_or_404(Candidate, pk=pk)
        if request.user.role != 'recruiter':
            return Response({'error': 'Only recruiters can reject candidates'}, status=status.HTTP_403_FORBIDDEN)

        candidate.stage = 'rejected'
        candidate.save()
        serializer = self.get_serializer(candidate)
        return Response(serializer.data)

# Web views for frontend
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('candidate_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set default role to candidate
            user.role = 'candidate'
            user.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('candidate_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class CandidateListView(ListView):
    model = Candidate
    template_name = 'candidates/candidate_list.html'
    context_object_name = 'candidates'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return Candidate.objects.filter(email=user.email)
        return Candidate.objects.all()

@method_decorator(login_required, name='dispatch')
class CandidateDetailView(DetailView):
    model = Candidate
    template_name = 'candidates/candidate_detail.html'
    context_object_name = 'candidate'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'candidate':
            return Candidate.objects.filter(email=user.email)
        return Candidate.objects.all()

@method_decorator(login_required, name='dispatch')
class CandidateCreateView(CreateView):
    model = Candidate
    template_name = 'candidates/candidate_form.html'
    fields = ['name', 'email', 'role', 'resume']
    success_url = reverse_lazy('candidate_list')

    def form_valid(self, form):
        messages.success(self.request, 'Candidate created successfully!')
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class CandidateUpdateView(UpdateView):
    model = Candidate
    template_name = 'candidates/candidate_form.html'
    fields = ['name', 'email', 'role', 'resume']
    success_url = reverse_lazy('candidate_list')

    def form_valid(self, form):
        messages.success(self.request, 'Candidate updated successfully!')
        return super().form_valid(form)

@login_required
def move_to_next_stage_view(request, pk):
    if request.user.role != 'recruiter':
        messages.error(request, 'Only recruiters can move candidates to next stage.')
        return redirect('candidate_list')

    candidate = get_object_or_404(Candidate, pk=pk)
    stage_order = ['applied', 'screening', 'interview', 'hired']
    current_index = stage_order.index(candidate.stage)

    if current_index < len(stage_order) - 1:
        candidate.stage = stage_order[current_index + 1]
        candidate.save()
        messages.success(request, f'Candidate moved to {candidate.stage} stage.')
    else:
        messages.warning(request, 'Candidate is already at the final stage.')

    return redirect('candidate_list')

@login_required
def reject_candidate_view(request, pk):
    if request.user.role != 'recruiter':
        messages.error(request, 'Only recruiters can reject candidates.')
        return redirect('candidate_list')

    candidate = get_object_or_404(Candidate, pk=pk)
    candidate.stage = 'rejected'
    candidate.save()
    messages.success(request, 'Candidate rejected.')

    return redirect('candidate_list')
