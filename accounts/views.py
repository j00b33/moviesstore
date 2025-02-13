from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, PasswordResetForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
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
            password = request.POST['password']
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
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST,
        error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('movies.index')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})


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
        # Instantiate the form
        form = PasswordResetForm()
        return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})

    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            
            try:
                user = User.objects.get(username=username)
                user.delete()
                
                new_user = User.objects.create_user(username=username, password=new_password)
                auth_login(request, new_user)
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('movies.index')
            except User.DoesNotExist:
                template_data['error'] = '* No account found with that username.'
                return render(request, 'accounts/reset.html', {'template_data': template_data, 'form': form})

# Create your views here.
