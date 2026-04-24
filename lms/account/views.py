from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import  UserInfo
from utilities.logger import logger
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import uuid
from .tasks import send_user_verification_email, send_password_reset_email, send_user_email_verification
from account.models import AllowedEmail
from course.models import Enrollment
from django.db.models import Q
# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password') 
        print(f'first_name: {first_name}\n last_name: {last_name} \n email: {email} \n password: {password}')
        
        e=False
        if User.objects.filter(username=username).exists():
            e=True
            messages.error(request, 'Username already exists!')
        if User.objects.filter(email=email).exists():
            e=True
            messages.error(request, 'Email already exists!')
        if e:
            return redirect('register')
        user_obj=None
        try:
            user_obj = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            UserInfo.objects.get_or_create(user=user_obj)
        except Exception as e:
            print(e)
            logger.error(f'Error in creating user: {e}')
            messages.error(request, 'Something went wrong.')
            return redirect('register')

        allowed_emails = AllowedEmail.objects.filter(email=email)
        if user_obj and allowed_emails.exists():
            allowed_emails.update(user=user_obj)
            Enrollment.objects.create(user=user_obj, course=allowed_emails.first().course)

        logger.info(f'New User Registered: {username}')
        messages.success(request, 'Account created successfully')
        return redirect('login')
    return render(request, 'auth/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('course_list')
    next_redirect = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user_obj = User.objects.filter(Q(email=username) | Q(username=username)).first()
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('login')
        
        # Ensure UserInfo exists (e.g. superuser created via CLI)
        try:
            user_info_obj = user_obj.user_info
        except UserInfo.DoesNotExist:
            user_info_obj = UserInfo.objects.create(user=user_obj, is_verified=True)

        # handling unverified users
        if not user_info_obj.is_verified:
            if user_info_obj.verification_code_expires_at is not None and user_info_obj.verification_code_expires_at > timezone.now():
                messages.info(request, 'Please verify your account.')
                return redirect('login')
            
            user_info_obj.verification_code = uuid.uuid4()
            user_info_obj.verification_code_created_at = timezone.now()
            user_info_obj.verification_code_expires_at = user_info_obj.verification_code_created_at + timezone.timedelta(minutes=5)
            user_info_obj.save()
            
            protocol = request.scheme
            domain = request.get_host()
            send_user_email_verification.delay(protocol, domain, user_obj.email, user_info.verification_code)
            
            messages.info(request, 'We sent you an email, please verify your account.')
            return redirect('login')
        
        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            # If remember me is not checked, expire session when browser closes
            if not remember:
                request.session.set_expiry(0)
            messages.success(request,'Login successfully.')
            logger.info(f'User Logged In: {username}')
            if next_redirect:
                return redirect(next_redirect)        
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credential')
            return redirect('login')
                
    return render(request, 'auth/login.html')

def logout_view(request):
    logger.info(f'User Logged Out: {request.user}')
    logout(request)
    return redirect('home')

def verify_view(request, token):
    user_info = UserInfo.objects.filter(verification_code=token, verification_code_expires_at__gte=timezone.now()).first()
    
    if user_info is None:
        return render(request, 'account/verification/failed.html')
    
    if user_info.is_verified:
        messages.error(request, 'Account already verified.')
        return redirect('login')
    
    user_info.is_verified = True
    user_info.verification_code_used_at = timezone.now()
    user_info.save()
    return render(request, 'account/verification/success.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.error(request, 'No account found with this email address.')
            return redirect('forgot_password')
        
        # Generate password reset token
        user_info = UserInfo.objects.filter(user=user_obj).first()
        if user_info is None:
            user_info = UserInfo.objects.create(user=user_obj)
        
        user_info.password_reset_token = uuid.uuid4()
        user_info.password_reset_token_created_at = timezone.now()
        user_info.password_reset_token_expires_at = user_info.password_reset_token_created_at + timezone.timedelta(minutes=30)
        user_info.save()
        
        # Send password reset email
        protocol = request.scheme
        domain = request.get_host()
        send_password_reset_email.delay(protocol, domain, email, str(user_info.password_reset_token))
        
        messages.success(request, 'Password reset link has been sent to your email.')
        return redirect('login')
    
    return render(request, 'auth/forgot_password.html')

def reset_password_view(request, token):
    user_info = UserInfo.objects.filter(
        password_reset_token=token,
        password_reset_token_expires_at__gte=timezone.now()
    ).first()
    
    if user_info is None:
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('login')
    
    if user_info.password_reset_token_used_at is not None:
        messages.error(request, 'This password reset link has already been used.')
        return redirect('login')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset_password_view', token=token)
        
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('reset_password_view', token=token)
        
        # Update password
        user_obj = user_info.user
        user_obj.set_password(new_password)
        user_obj.save()
        
        # Mark token as used
        user_info.password_reset_token_used_at = timezone.now()
        user_info.save()
        
        logger.info(f'Password reset successful for user: {user_obj.username}')
        messages.success(request, 'Password reset successful! You can now login with your new password.')
        return redirect('login')
    
    return render(request, 'auth/reset_password.html')

@login_required(login_url='login')
def my_courses(request):
    enrollments = request.user.enrollments.all()
    context = {
        'enrollments': enrollments
    }
    return render(request, 'account/my_courses.html', context)
