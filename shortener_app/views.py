from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from shortener_app.forms import SignUpForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def splash(request):
    return render(request, 'splash.html')


@login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            print('logged in')
            return redirect('home')
        else:
            print('user is none')
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            hashed_pass = make_password(form.cleaned_data['password'])
            new_user = User(email=form.cleaned_data['email'], username=form.cleaned_data['email'], password=hashed_pass)
            new_user.save()
            return render(request, 'login')

    return render(request, 'signup.html', {'form': form})

