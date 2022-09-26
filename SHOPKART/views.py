from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


# Create your views here.
@never_cache
def startingpage(request):
    if 'sessionlog' in request.session:
        print(request.session)
        return redirect(to='home')
    
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        if len(username) == 0 or len(password) == 0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='start')
        else:
            user = auth.authenticate(username=username, password=password)
            
            if user is not None and user.is_superuser==False:
                auth.login(request, user)
                request.session['sessionlog'] = username
                return redirect(to='home')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect(to='start')
                
        
    else:
        return render(request, 'login.html')

@never_cache
def signuppage(request):
   if request.method == 'POST':
       first_name = request.POST['firstname']
       print(first_name)
       last_name = request.POST['lastname']
       print(last_name)
       email = request.POST['email']
       print(email)
       username = request.POST['username']
       print(username)
       password = request.POST['password']
       print(password)
     
       if User.objects.filter(username=username).exists():
           messages.info(request, 'Error : Username already Taken')
           return redirect('signup')
       else:
            print(password)
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, )
            user.save()
            print('success')
            return redirect(to='start')
   else:
        return render(request, 'signup.html')
@login_required(login_url='start')
@never_cache
def homepage(request):
    return render(request, 'home.html')
@login_required(login_url='start')
@never_cache
def logout(request):
    request.session.flush()
    auth.logout(request)
    return redirect(to='start')   
     
       







