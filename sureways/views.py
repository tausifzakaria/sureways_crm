from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def Home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        return render(request, 'home.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'authentication/login.html')

def Logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')