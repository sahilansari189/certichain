from django.shortcuts import render
from utilities.logger import logger
from course.models import Course
from credential.models import Certificate
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def overview(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'base/Placeholders/overview.html', context)

@login_required(login_url='login')
def digital_credentials(request):
    certificates = Certificate.objects.filter(user=request.user)

    context = {
        'certificates': certificates,   
    }
    return render(request, 'base/Placeholders/digital_credentials.html', context)

def faq(request):
    return render(request, 'base/Placeholders/FAQ.html')


