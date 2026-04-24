import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from .tasks import send_contact_email_task
logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            # Basic validation
            if not all([name, email, subject, message]):
                messages.error(request, "All fields are required.")
                logger.warning("Contact form submission failed: Missing fields.")
                return render(request, 'contact/contact.html', {
                    'name': name, 'email': email, 'subject': subject, 'message': message
                })

            # Save to database
            contact_entry = Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            logger.info(f"Contact message received from {email} (ID: {contact_entry.id})")
            send_contact_email_task(name, email, subject, message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')

        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}", exc_info=True)
            messages.error(request, "An error occurred while sending your message. Please try again later.")
            return render(request, 'contact/contact.html')

    return render(request, 'contact/contact.html')

