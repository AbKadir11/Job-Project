from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company


# register applicant only
def register_applicant(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            var.is_applicant = True
            var.username = var.email
            var.save()
            Resume.objects.create(user=var)
            messages.info(request, 'Your Account Has Been Created.')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong.')
            return redirect('register-applicant')
        
    else:
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, 'user/register_applicant.html', context)
    
    
# register recruiter only
def register_recruiter(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            var = form.save(commit = False)
            var.is_recruiter = True
            var.username = var.email
            var.save()
            Company.objects.create(user=var)    
            messages.info(request, 'Your Account Has Been Created.')
            return redirect('login')
        else:
            messages.warning(request, 'Something went wrong.')
            return redirect('register-recruiter')
        
    else:
        form = RegisterUserForm()
        context = {'form': form}
        return render(request, 'user/register_recruiter.html', context) 
    

# login a user

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username= email, password= password)
        
        if user is not None and user.is_active:
            login(request, user)
            # if request.user.is_applicant:
            #     return redirect('applicant-dashboard')
            # elif request.user.is_recruiter:
            #     return redirect('recruiter-dashboard')
            # else:
            #     return redirect('login')
            return redirect('dashboard')
        
        else:
            messages.warning(request, 'Something went wrong.')
            return redirect('login')
    
    else:
        return render(request, 'user/register_recruiter.html') 
    
    

# logout a user

def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended')
    return redirect('login')
        
    
