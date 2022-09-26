from ast import Return
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



def adminstart(request):
    if 'sessionadmin' in request.session:
        return redirect(to='home')
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        if len(username) == 0 or len(password) == 0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='adminstart')
        
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            request.session['sessionadmin'] = username
            return redirect('adminhome')
            
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'adminlogin.html')
    else:
        
       return render (request,"adminlogin.html")



@login_required(login_url='adminstart')
@never_cache
def adminhome(request):
    if 'search' in request.POST:
         search = request.POST['search']
         users = User.objects.filter(username__contains=search)
         print("==",users)
         if len(users)!=0 :
             return render(request, 'adminhome.html',{'users':users})
         else:
            messages.info(request, "No Matches found")
            return redirect('adminhome')
    else:
        users=User.objects.filter(is_superuser=False)
        return render(request, 'adminhome.html',{'users':users})

@login_required(login_url='adminstart')
@never_cache
def edituser(request):
    id=request.GET['id']
    if request.method=='POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        email=request.POST['email']
        username=request.POST['uname']
        password=request.POST['password']
        
        user = User.objects.create_user(id=id,username=username, password=password, first_name=fname, last_name=lname, email=email)
        print(user.password)
        user.save_base()
        print('success')
        return redirect('adminhome')
    else:
        user=User.objects.filter(id=id)
        return render(request, 'edituser.html',{'user':user})
    
@login_required(login_url='adminstart')
@never_cache
def adduser(request):
    if request.method=='POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        username = request.POST['uname']
        password = request.POST['password']
        if len(username) == 0 or len(password) == 0 or len(first_name)==0 or len(last_name)==0 or len(email)==0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='adduser')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username Taken')
            return redirect('adduser')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Exists')
            return redirect('adduser')
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.save()
            print(password)
            return redirect(to='adminhome')
    else:
        return render(request, 'adduser.html')

@login_required(login_url='adminstart')
@never_cache
def adminout(request):
    request.session.flush()
    auth.logout(request)
    return redirect('adminstart')

@login_required(login_url='adminstart')
def deleteuser(request):
    id=request.GET['id']
    user=User.objects.filter(id=id)
    user.delete()
    return redirect('adminhome')