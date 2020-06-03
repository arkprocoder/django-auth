from django.shortcuts import render,HttpResponse,redirect
# from .models import Contact
from django.views.generic import View
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.
# def index(request):
    
#     return render(request,'index.html')


class RegistrationView(View):
    def get(self,request):
        
        return render(request,'index.html')

    def post(self,request):
        context = {
        'data': request.POST,
        'has_error':False
        }
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if len(username) > 15:
            messages.error(request,"Your UserName must be Under 10 characters")
            context['has_error']=True
           

        if not username.isalnum():
            messages.error(request,"Username should only contain letters and number.")
            context['has_error']=True

        if pass1 != pass2:
            
            messages.error(request,"Password do not Match,Please Try Again!")
            context['has_error']=True
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Username Already Taken")
                context['has_error']=True
        except Exception as identifier:
            pass 

        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                context['has_error']=True
        except Exception as identifier:
            pass        

        if context['has_error']:
            return render(request,'index.html')

            

        # checks for error inputs
        user=User.objects.create_user(username=username,email=email)
        user.set_password(pass1)
        user.first_name=fname
        user.last_name=lname
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subject='Activate Your Account',
       
        message=render_to_string('activate.html', 
        {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)

        }
        
        )
        emailuser=EmailMessage(
            email_subject,message,settings.EMAIL_HOST_USER,[email],
        )
        emailuser.send()
        messages.success(request,"Your Account has been Succesfully Created")
        return redirect('/home')

        # else:
        # messages.error(request,"not found")
        # return render(request,"index.html")        


            
        # messages.warning(request,"SUCCESSFULLY ACCOUNT CREATED")  
        # return redirect('/home')
   
        return render(request,'index.html',context)    

def handleSignup(request):
    if request.method == 'POST':

        # get parameters
        username=request.POST.get('username','')
        fname=request.POST.get('fname','')
        lname=request.POST.get('lname','')
        email=request.POST.get('email','')
        pass1=request.POST.get('pass1','')
        pass2=request.POST.get('pass2','')
        if len(username) > 15:

            messages.error(request,"Your UserName must be Under 10 characters")
           
            return redirect('/')

        if not username.isalnum():
            messages.error(request,"Username should only contain letters and number.")
            return redirect('/')    


        if pass1 != pass2:
            
            messages.error(request,"Password do not Match,Please Try Again!")
            return redirect('/')
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Username Already Taken")
                return redirect('/')
        except Exception as identifier:
            pass 

        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/')
        except Exception as identifier:
            pass        


        # checks for error inputs
        user=User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subject='Activate Your Account',
       
        message=render_to_string('activate.html', 
        {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)

        }
        
        )
        emailuser=EmailMessage(
            email_subject,message,settings.EMAIL_HOST_USER,[email],
        )
        emailuser.send()
        messages.success(request,"Your Account has been Succesfully Created")
        return redirect('/')

    else:
        messages.error(request,"not found")
        return render(request,"index.html")        


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Activated Successfilly")
            return redirect('/')
        return render(request,'activatefail.html',status=401)                
          
def handleLogin(request):
      if request.method == 'POST':

        # get parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/')    

         

      return HttpResponse('404-Not Found')        


def handleLogout(request):
    
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('/')
    
        
    return HttpResponse('404-Not Found')


class LoginView(View):
    def get(self,request):

        return render(request,'home.html')