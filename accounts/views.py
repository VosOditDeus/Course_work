from django.http.response import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context_processors import csrf
from Course.forms import LogInForm, UserRegistrationForm
from Course.models import profile
from django.contrib.auth import authenticate, login

def user_login(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return  HttpResponse('Disabled account')
            else:
                return  HttpResponse('Invalid login')
    else:
        form = LogInForm()
    args['form'] = form

    return render_to_response('login.html',args)


def registration(request):
    args = {}
    args.update(csrf(request))
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            #Create profile for User
            profile.objects.create(user=new_user)
            args['new_user'] = new_user
            return render_to_response('registration/register_done.html', args)
    else:
        user_form = UserRegistrationForm()
    args['user_form'] = user_form
    return render_to_response('registration/register.html', args)
