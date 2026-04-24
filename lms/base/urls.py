from django.urls import path
from .views import home,overview,digital_credentials,faq
from account.views import register_view,login_view
urlpatterns = [
    #base urls
    path('', home , name='home'),
    
    #auth urls
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),

    #footer urls
    path('overview/', overview, name='overview'),
    path('digital-credentials/', digital_credentials, name='digital_credentials'),
    path('frequently-asked-questions/', faq, name='faq'),
]
