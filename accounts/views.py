from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password'],
        )
        if user is None:
            template_data['error'] = '* The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('movies.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'

    if request.method == 'GET':
        # On GET, display the form to the user
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    elif request.method == 'POST':
        # On POST, handle the form submission
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)

        if form.is_valid():
            # Save the user object first
            user = form.save()

            # Now create a UserProfile and save the security question and answer
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Update the UserProfile with the security question and answer
            user_profile.security_question = form.cleaned_data['security_question']
            user_profile.security_answer = form.cleaned_data['security_answer']
            user_profile.save()
            # Optionally log the user in after account creation
            auth_login(request, user)

            # Success message and redirect
            messages.success(request, 'Account created successfully.')
            return redirect('movies.index')  # Or your desired page
        else:
            # If the form is invalid, return the form with errors
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

        
def reset(request):
    template_data = {}
    template_data['title'] = 'Reset Password'

    if request.method == 'GET':
        form = PasswordResetForm()
        return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})

    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            security_answer = form.cleaned_data.get('security_answer')

            try:
                user = User.objects.get(username=username)
                # Assuming the security question and answer are stored in a UserProfile or another place
                user_profile = user.userprofile  # Assuming you have a UserProfile model for this

                # Strip leading/trailing spaces and compare case-insensitively
                stored_answer = user_profile.security_answer.strip().lower()
                user_answer = security_answer.strip().lower()

                if user_answer == stored_answer:
                    # Answer is correct, reset password
                    user.set_password(new_password)
                    user.save()
                    auth_login(request, user)
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('movies.index')
                else:
                    print("Stored Answer:", user_profile.security_answer)
                    print("User Answer:", user_answer)
                    template_data['error'] = '* The security answer is incorrect.'
                    return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})

            except User.DoesNotExist:
                template_data['error'] = '* No account found with that username.'
                return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})
