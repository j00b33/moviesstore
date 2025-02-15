from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
#SIGNUP FUNCTION AT 35 - 69, RESET PASSWORD FUNCTION (i think this works) IS 81 - END
#THIS IS WHERE THE MAIN PROBLEM IS AT
#IN THE SIGNUP FUNCTION, THE PRINT STATEMENTS SHOW THAT BOTH THE FORM AND THE USERPROFILE
#CORRECTLY SAVE THE SECURITY QUESTION/ANSWER. HOWEVER, IF YOU TRY TO DO RESET, THE PRINT STATEMENT
#THERE SHOWS THAT THERE IS NO SECURITY QUESTION/ANSWER SAVED. ALSO, IF YOU MANUALLY LOOK IN THE ADMIN PANEL,
#THE SECURITY QUESTION AND ANSWER ARE NOT SAVED AFTER LOGIN. IF YOU MANUALLY ENTER A SECURITY QUESTION/ANSWER,
#THESE WILL SHOW UP CORRECTLY AND WILL BE SHOWN BY THE PRINT STATEMENT IN THE RESET PASSWORD FUNCTION.
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
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)

        if form.is_valid():
            user = form.save()

            # Now create a UserProfile and save the security question and answer
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            # Update the UserProfile with the security question and answer
            user_profile.security_question = form['security_question']
            user_profile.security_answer = form['security_answer']
            user_profile.save()
            #Security question and answer are both processed correctly, it just dont save
            #THIS IS THE PART THATS BROKE AND ITS ANNOYING AS SHIT
            print(form['security_question'])
            print(form['security_answer'])
            print(user_profile.security_question)
            print(user_profile.security_answer)

            auth_login(request, user)

            messages.success(request, 'Account created successfully.')
            return redirect('movies.index')  
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    print(request.user.userprofile.security_question)
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
                user_profile = user.userprofile  

                stored_answer = user_profile.security_answer.strip().lower()
                user_answer = security_answer.strip().lower()

                if user_answer == stored_answer:
                    user.set_password(new_password)
                    user.save()
                    auth_login(request, user)
                    messages.success(request, 'Your password has been reset successfully.')
                    return redirect('movies.index')
                else:
                    #The entered user answer is correct, the user_profile security answer is empty when checking in admin
                    print("Stored Answer:", user_profile.security_answer)
                    print("User Answer:", user_answer)
                    template_data['error'] = '* The security answer is incorrect.'
                    return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})

            except User.DoesNotExist:
                template_data['error'] = '* No account found with that username.'
                return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})
