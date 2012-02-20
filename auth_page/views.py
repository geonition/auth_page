from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login_view
from django.contrib.auth.views import password_reset
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from forms import ProfileForm
from models import Email
from random import random

def login(request):
    return django_login_view(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(form.cleaned_data['username'],
                                    '',
                                    password=form.cleaned_data['password1'])
            
            #form.save()
            
            new_user = authenticate(username = request.POST.get('username'),
                                    password = request.POST.get('password1'))
            django_login(request, new_user)
            
            return HttpResponseRedirect(request.POST.get('next', '/'))
        else:            
            next = request.GET.get('next', '/')
            return render_to_response('register.html',
                                      {'form': form,
                                        'next': next},
                                        context_instance = RequestContext(request))
    else:
        form = UserCreationForm()
        next = request.GET.get('next', '/')
        return render_to_response('register.html',
                                  {'form': form,
                                    'next': next},
                                    context_instance = RequestContext(request))
    

def logout(request):
    django_logout(request)
    return  HttpResponseRedirect(request.GET.get('next', '/'))
    

def profile(request):
    """
    Form for modifying and adding profile values
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST,
                           instance = request.user)
        
        email = request.POST.get('email', '')
        if not email == '' and not email == request.user.email:
            #confirm the email
            salt = sha_constructor(str(random())).hexdigest()[:5]
            confirmation_key = sha_constructor(salt + email).hexdigest()
            current_site = Site.objects.get_current()
       
            path = reverse('confirm_email',
                            args=[confirmation_key])
                
            activate_url = u"http://%s%s" % (unicode(current_site.domain),
                                             path)
            context = {
                "user": request.user,
                "activate_url": activate_url,
                "current_site": current_site,
                "confirmation_key": confirmation_key,
            }
            subject = render_to_string(
                "email_confirmation_subject.txt",
                context)
        
            # remove superfluous line breaks
            subject = "".join(subject.splitlines())
            message = render_to_string(
                "email_confirmation_message.txt",
                context)
            print email
            send_mail(subject,
                      message,
                      getattr(settings,
                              'DEFAULT_FROM_EMAIL',
                              'do-not-reply@%s' % current_site),
                      [email])
        
            Email.objects.create(
                owner = request.user,
                email = email,
                email_is_verified = False,
                sent = datetime.now(),
                confirmation_key = confirmation_key)
        
        form.save()
        return HttpResponseRedirect(request.POST.get('next', '/'))

    else:
        form = ProfileForm(instance = request.user)
        next = request.GET.get('next', '/')
        return render_to_response('profile.html',
                                  {'form': form,
                                   'next': next},
                                  context_instance = RequestContext(request))
        
def confirm_email(request, confirmation_key):
    try:
        email = Email.objects.get(confirmation_key = confirmation_key,
                                  email_is_verified = False)
        email.email_is_verified = True
        email.save()
        return render_to_response('email_confirmed.html',
                                  {'email': email})
    except Email.DoesNotExist:
        return HttpResponse('No email found for this link')

def retrieve_new_password(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        try:
            verified_email = Email.objects.get(email = email,
                                               email_is_verified = True)
            return password_reset(request)
        except Email.DoesNotExist:
            return render_to_response('retrieve_new_password.html',
                                      {'errors': 'The email you entered was not found or it has never been verified'},
                                      context_instance = RequestContext(request))
    else:
        return render_to_response('retrieve_new_password.html',
                                  context_instance = RequestContext(request))
    