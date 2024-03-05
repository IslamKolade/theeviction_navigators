from django.shortcuts import render, get_object_or_404
from .models import The_Eviction_Navigators, Contact_Form_Submission
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField


# Create your views here.
def home(request):
    the_eviction_navigators = get_object_or_404(The_Eviction_Navigators, pk=1)
    return render(request, 'index.html', {'the_eviction_navigators': the_eviction_navigators})


def contact_form_submission(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')
        eviction_type = request.POST.get('eviction_type')
        captcha_response = request.POST.get('g-recaptcha-response')

        the_eviction_navigators = get_object_or_404(The_Eviction_Navigators, pk=1)

        # Validate the reCAPTCHA response
        recaptcha = ReCaptchaField()
        recaptcha.public_key = settings.RECAPTCHA_PUBLIC_KEY
        recaptcha.private_key = settings.RECAPTCHA_PRIVATE_KEY
        if not recaptcha.clean(captcha_response):
            return render(request, 'index.html', {'the_eviction_navigators': the_eviction_navigators})

        contact_form = Contact_Form_Submission(
            name = name,
            email = email,
            phone_number = phone_number,
            message = message,
            eviction_type = eviction_type,
        )
       
        contact_form.save()

        email_subject = 'Contact Form Submission'
        email_body = render_to_string('email_template.html', {
            'name': name,
            'email': email,
            'phone_number': phone_number,
            'message': message,
            'the_eviction_navigators_phone_number' : the_eviction_navigators.phone_number,
            'eviction_type': eviction_type,
        })

        # Send the email
        msg = EmailMessage(email_subject, email_body, to=[email, 'angie.evictionavigator@gmail.com'])
        msg.content_subtype = 'html'
        msg.send()

        return render(request, 'index.html', {'the_eviction_navigators': the_eviction_navigators})






