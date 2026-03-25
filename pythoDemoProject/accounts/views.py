from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout

from .forms import RegisterForm
# Create your views here.
def register_view(request):
    form=RegisterForm()

    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
        
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user=authenticate(request,username=username,password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })
        
    return render(request, 'accounts/login.html')

        

def logout_view(request):
    logout(request)
    return redirect('login')