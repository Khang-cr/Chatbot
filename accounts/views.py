from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm, TherapistVerificationForm
from .models import UserProfile, DASS21Result
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('student_basic_info')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        user_type = self.request.POST.get('user_type', 'student')
        UserProfile.objects.create(user=user, user_type=user_type)
        # Login
        login(self.request, user)
        
        # Redirect dựa vào user_type
        if user_type == 'therapist':
            return redirect('therapist_basic_info')
        else:
            return redirect('student_basic_info')

@login_required
def therapist_verification_view(request):
    profile = request.user.userprofile

    if profile.user_type != 'therapist':
        messages.error(request, 'This page is only for therapists!')
        return redirect('homepage')
    
    if request.method == 'POST':
        form = TherapistVerificationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.verification_status = 'pending'
            profile.save()
            messages.success(request, 'Verification document submitted successfully! Please wait for approval.')
            return redirect('verification_pending')
        else:
            messages.error(request, 'Please upload a valid image file.')
    else:
        form = TherapistVerificationForm(instance=profile)
    
    return render(request, 'registration/therapist_verification.html', {'form': form})

@login_required
def verification_pending_view(request):
    profile = request.user.userprofile

    if profile.user_type != 'therapist':
        return redirect('homepage')
    return render(request, 'registration/verification_pending.html', {'status': profile.verification_status})


@login_required
def therapist_basic_info_view(request):
    profile = request.user.userprofile
    
    if profile.user_type != 'therapist':
        messages.error(request, 'This page is only for therapists!')
        return redirect('homepage')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        age = request.POST.get('age', '')
        gender = request.POST.get('gender', '')
        occupation = request.POST.get('occupation', '')
        university = request.POST.get('university', '')
        phone = request.POST.get('phone', '')
        
        # Save to User model
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Save to UserProfile
        profile.age = age
        profile.gender = gender
        profile.occupation = occupation
        profile.university = university
        profile.phone = phone
        profile.save()
        
        # Redirect to verification page
        return redirect('therapist_verification')
    
    return render(request, 'registration/therapist_basic_info.html')


@login_required
def student_basic_info_view(request):
    profile = request.user.userprofile
    if profile.user_type != 'student':
        messages.error(request, 'This page is only for students!')
        return redirect('homepage')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        age = request.POST.get('age', '')
        gender = request.POST.get('gender', '')
        occupation = request.POST.get('occupation', '')
        university = request.POST.get('university', '')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # UserProfile updating
        profile = request.user.userprofile
        profile.age = age
        profile.gender = gender
        profile.occupation = occupation
        profile.university = university
        profile.save()
        
        # register then do test
        return redirect('dass21_test')
    
    return render(request, 'registration/student_basic_info.html')

@login_required
def dass21_test_view(request):
    if request.method == 'POST':
        # get answer
        answers = {}
        for i in range(1, 22):
            answers[f'q{i}'] = int(request.POST.get(f'q{i}', 0))
        
        # cal score
        scores = calculate_dass21_scores(answers)
        
        # store result
        DASS21Result.objects.create(
            user=request.user,
            answers=answers,
            depression_score=scores['depression'],
            anxiety_score=scores['anxiety'],
            stress_score=scores['stress'],
            depression_level=scores['depression_level'],
            anxiety_level=scores['anxiety_level'],
            stress_level=scores['stress_level']
        )
        
        # redirect to the result page
        return redirect('dass21_result')
    
    # DASS-21 questions
    questions = get_dass21_questions()
    
    return render(request, 'registration/DASS-21_TEST.html', {'questions': questions})

@login_required
def dass21_result_view(request):
    try:
        result = DASS21Result.objects.filter(user=request.user).latest('test_date')
        recommendations = get_recommendations(result)
        
        context = {
            'result': result,
            'recommendations': recommendations
        }
        return render(request, 'registration/Test_Result.html', context)
    except DASS21Result.DoesNotExist:
        return redirect('dass21_test')

@login_required
def profile_detail_view(request):
    user = request.user
    profile = user.userprofile
    
    if profile.user_type == 'therapist':
        # Therapist profile
        context = {
            'user': user,
            'profile': profile,
        }
        return render(request, 'registration/therapist_profile.html', context)
    else:
        # Student profile
        test_history = DASS21Result.objects.filter(user=user).order_by('-test_date')
        context = {
            'user': user,
            'profile': profile,
            'test_history': test_history,
        }
        return render(request, 'registration/student_profile.html', context)
    
# Helper functions

def get_dass21_questions():
    return [
        # Depression (questions: 3, 5, 10, 13, 16, 17, 21)
        {'id': 1, 'text': 'I found it hard to wind down', 'category': 'stress'},
        {'id': 2, 'text': 'I was aware of dryness of my mouth', 'category': 'anxiety'},
        {'id': 3, 'text': "I couldn't seem to experience any positive feeling at all", 'category': 'depression'},
        {'id': 4, 'text': 'I experienced breathing difficulty', 'category': 'anxiety'},
        {'id': 5, 'text': 'I found it difficult to work up the initiative to do things', 'category': 'depression'},
        {'id': 6, 'text': 'I tended to over-react to situations', 'category': 'stress'},
        {'id': 7, 'text': 'I experienced trembling (e.g., in the hands)', 'category': 'anxiety'},
        {'id': 8, 'text': 'I felt that I was using a lot of nervous energy', 'category': 'stress'},
        {'id': 9, 'text': 'I was worried about situations in which I might panic', 'category': 'anxiety'},
        {'id': 10, 'text': 'I felt that I had nothing to look forward to', 'category': 'depression'},
        {'id': 11, 'text': 'I found myself getting agitated', 'category': 'stress'},
        {'id': 12, 'text': 'I found it difficult to relax', 'category': 'stress'},
        {'id': 13, 'text': 'I felt down-hearted and blue', 'category': 'depression'},
        {'id': 14, 'text': 'I was intolerant of anything that kept me from getting on with what I was doing', 'category': 'stress'},
        {'id': 15, 'text': 'I felt I was close to panic', 'category': 'anxiety'},
        {'id': 16, 'text': 'I was unable to become enthusiastic about anything', 'category': 'depression'},
        {'id': 17, 'text': "I felt I wasn't worth much as a person", 'category': 'depression'},
        {'id': 18, 'text': 'I felt that I was rather touchy', 'category': 'stress'},
        {'id': 19, 'text': 'I was aware of the action of my heart in the absence of physical exertion', 'category': 'anxiety'},
        {'id': 20, 'text': 'I felt scared without any good reason', 'category': 'anxiety'},
        {'id': 21, 'text': 'I felt that life was meaningless', 'category': 'depression'},
    ]

def calculate_dass21_scores(answers):
    # questions for each one
    depression_qs = [3, 5, 10, 13, 16, 17, 21]
    anxiety_qs = [2, 4, 7, 9, 15, 19, 20]
    stress_qs = [1, 6, 8, 11, 12, 14, 18]
    
    # sum score
    depression = sum(answers[f'q{i}'] for i in depression_qs) * 2
    anxiety = sum(answers[f'q{i}'] for i in anxiety_qs) * 2
    stress = sum(answers[f'q{i}'] for i in stress_qs) * 2
    
    # Determine level
    def get_level(score, thresholds):
        if score < thresholds[0]:
            return 'Normal'
        elif score < thresholds[1]:
            return 'Mild'
        elif score < thresholds[2]:
            return 'Moderate'
        elif score < thresholds[3]:
            return 'Severe'
        else:
            return 'Extremely Severe'
    
    # Score level for each one
    depression_thresholds = [10, 14, 21, 28]
    anxiety_thresholds = [8, 10, 15, 20]
    stress_thresholds = [15, 19, 26, 34]
    
    return {
        'depression': depression,
        'anxiety': anxiety,
        'stress': stress,
        'depression_level': get_level(depression, depression_thresholds),
        'anxiety_level': get_level(anxiety, anxiety_thresholds),
        'stress_level': get_level(stress, stress_thresholds),
    }

def get_recommendations(result):
    recommendations = []
    
    # Depression
    if result.depression_level in ['Severe', 'Extremely Severe']:
        recommendations.append({
            'type': 'depression',
            'level': 'high',
            'message': 'You are experiencing severe depression. We strongly recommend seeking professional help immediately.',
            'actions': [
                'Contact university counseling center',
                'Speak with a mental health professional',
                'Reach out to trusted friends or family',
            ]
        })
    elif result.depression_level == 'Moderate':
        recommendations.append({
            'type': 'depression',
            'level': 'medium',
            'message': 'You are experiencing moderate depression. Consider talking to a counselor.',
            'actions': [
                'Schedule an appointment with campus counselor',
                'Practice self-care activities',
                'Join support groups',
            ]
        })
    
    # Anxiety
    if result.anxiety_level in ['Severe', 'Extremely Severe']:
        recommendations.append({
            'type': 'anxiety',
            'level': 'high',
            'message': 'You are experiencing severe anxiety. Professional support is recommended.',
            'actions': [
                'Learn relaxation techniques',
                'Consider cognitive behavioral therapy',
                'Practice mindfulness meditation',
            ]
        })
    
    # Stress
    if result.stress_level in ['Severe', 'Extremely Severe']:
        recommendations.append({
            'type': 'stress',
            'level': 'high',
            'message': 'You are experiencing high stress levels. Take steps to manage your stress.',
            'actions': [
                'Identify stress triggers',
                'Improve time management',
                'Get regular exercise',
                'Ensure adequate sleep',
            ]
        })
    
    # all normal
    if not recommendations:
        recommendations.append({
            'type': 'general',
            'level': 'low',
            'message': 'Your mental health appears to be within normal range. Keep up the good work!',
            'actions': [
                'Maintain healthy lifestyle habits',
                'Continue stress management practices',
                'Stay connected with support network',
            ]
        })
    
    return recommendations
