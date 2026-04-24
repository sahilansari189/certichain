from django.shortcuts import render

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, '404.html', status=404)

