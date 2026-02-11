from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Candidate

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('Candidate', 'Candidate'), ('Recruiter', 'Recruiter')], required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group_name = form.cleaned_data['role']
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            login(request, user)
            messages.success(request, 'Account created successfully.')
            return redirect('candidate_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def candidate_list(request):
    is_recruiter = request.user.groups.filter(name='Recruiter').exists()
    if is_recruiter:
        candidates = Candidate.objects.all()
    else:
        candidates = Candidate.objects.filter(user=request.user)
    return render(request, 'candidates/candidate_list.html', {'candidates': candidates, 'is_recruiter': is_recruiter})

@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if not request.user.groups.filter(name='Recruiter').exists() and candidate.user != request.user:
        return redirect('candidate_list')
    return render(request, 'candidates/candidate_detail.html', {'candidate': candidate})

@login_required
def candidate_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        role = request.POST['role']
        resume_text = request.POST['resume_text']
        candidate = Candidate.objects.create(
            user=request.user,
            name=name,
            email=email,
            role=role,
            resume_text=resume_text
        )
        messages.success(request, 'Candidate created successfully.')
        return redirect('candidate_detail', pk=candidate.pk)
    return render(request, 'candidates/candidate_form.html')

@login_required
def candidate_update(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if not request.user.groups.filter(name='Recruiter').exists() and candidate.user != request.user:
        return redirect('candidate_list')
    if request.method == 'POST':
        candidate.name = request.POST['name']
        candidate.email = request.POST['email']
        candidate.role = request.POST['role']
        candidate.resume_text = request.POST['resume_text']
        candidate.save()
        messages.success(request, 'Candidate updated successfully.')
        return redirect('candidate_detail', pk=candidate.pk)
    return render(request, 'candidates/candidate_form.html', {'candidate': candidate})

@login_required
def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if not request.user.groups.filter(name='Recruiter').exists():
        return redirect('candidate_list')
    if request.method == 'POST':
        candidate.delete()
        messages.success(request, 'Candidate deleted successfully.')
        return redirect('candidate_list')
    return render(request, 'candidates/candidate_confirm_delete.html', {'candidate': candidate})

@login_required
def move_stage(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if not request.user.groups.filter(name='Recruiter').exists():
        return redirect('candidate_list')
    if request.method == 'POST':
        new_status = request.POST['status']
        if new_status in dict(Candidate.STATUS_CHOICES):
            candidate.status = new_status
            candidate.save()
            messages.success(request, f'Candidate moved to {candidate.get_status_display()}.')
        return redirect('candidate_detail', pk=candidate.pk)
    return render(request, 'candidates/move_stage.html', {'candidate': candidate})
