from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template.context_processors import csrf
from django.template.defaultfilters import slugify
from actions.utils import *
from Course_work.settings import MEDIA_URL
from Course.forms import CommentForm, LogInForm, UserRegistrationForm, ProfileEditForm, UserEditForm , UploadWorkForm,MSingUpForm
from .models import competition, work,profile,work_for_competition
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from .tasks import work_uploaded

def index(request):
    args = {}
    args.update(csrf(request))
    competition_list = competition.objects.all()
    args['comp'] = competition_list
    args['backurl'] = request.META.get("HTTP_REFERER")
    return render_to_response('index.html', args, context_instance=RequestContext(request))

def competition_detail(request,slug):
    args = {}
    args.update(csrf(request))
    competition_detailed = get_object_or_404(competition, slug=slug)
    comments = competition_detailed.comments.filter(active=True)
    if request.method == 'POST':
        # A comment was posted

        sing_up_form = MSingUpForm(request.POST)
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
        # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
        # Assign the current post to the comment
            new_comment.competition = competition_detailed
            new_comment.name = request.user.get_full_name()
            new_comment.email = request.user.email
        # Save the comment to the database
            new_comment.save()
            sing_up_form.save()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()
        sing_up_form = MSingUpForm()
    args['backurl'] = request.META.get("HTTP_REFERER")
    args['comp'] = competition_detailed
    args['comments'] = comments
    args['comment_form'] = comment_form
    args['media_url'] = MEDIA_URL
    args['sing_up'] = sing_up_form
    return render_to_response('competition_detail.html', args, context_instance=RequestContext(request))

def competition_list(request):
    args = {}
    args.update(csrf(request))
    competition_list = competition.objects.all()
    paginator = Paginator(competition_list, 10) # per page.
    page = request.GET.get('page')
    try:
        competitions = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        competitions = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        competitions = paginator.page(paginator.num_pages)
    args['compl'] = competition_list
    args['page'] = page
    args['competitions'] = competitions
    return render_to_response('competition_list.html', args, context_instance=RequestContext(request))

def work_detail(request,slug):
    args = {}
    args.update(csrf(request))
    work_detail = work.objects.get(slug=slug)
    args['work'] = work_detail
    return render_to_response('work_detail.html', args, context_instance=RequestContext(request))

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
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LogInForm()
    args['form'] = form

    return render_to_response('login.html', args, context_instance=RequestContext(request))

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
            create_action(request.user.get_full_name(), 'have just registered!')
            return render_to_response('registration/register_done.html', args)
    else:
        user_form = UserRegistrationForm()
    args['user_form'] = user_form
    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))

@login_required
def edit(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Successfully updated')
            create_action(request.user, ' has edited his profile')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    args['user_form'] = user_form
    args['profile_form'] = profile_form
    return render_to_response('registration/edit.html', args, context_instance=RequestContext(request))

def student_list(request):
    args = {}
    args.update(csrf(request))
    student_list = profile.objects.all().filter(is_student=True)
    args['list'] = student_list
    return render_to_response('list_student.html', args, context_instance=RequestContext(request))


def student_detail(request, user):
    args = {}
    args.update(csrf(request))
    student_detail = get_object_or_404(profile, user__username=user)
    args['student'] = student_detail
    args['media_url'] = MEDIA_URL
    return render_to_response('student_detail.html', args, context_instance=RequestContext(request))



def sing_up(request,comp_id):
    args = {}
    args.update(csrf(request))
    choosen_competiion = competition.objects.get(id=comp_id)
    if request.method == 'POST':
        MSingUpForm.base_fields['work_name'] = forms.ModelChoiceField(queryset=work.objects.filter(author=profile.objects.get(user=request.user)))
        form = MSingUpForm(request.POST)
        r = request.POST.get('work_name')
        if form.is_valid():
            #TODO: Still bug with non request user works
            f1 = form.save(commit=False)
            f1.competition = choosen_competiion
            f1.work_name = work.objects.get(id=r)
            f1.save()
            choosen_competiion.students.add(request.user.profile)
            create_action(request.user, 'singed up on ', f1.competition)
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse('Failed')


def upload_work(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        work_form = UploadWorkForm(data=request.POST, files=request.FILES)
        if work_form.is_valid():
            new_work = work_form.save(commit=False)
            new_work.author = request.user.profile
            new_work.slug = slugify(new_work.name)
            new_work.save()
            create_action(request.user, 'have uploaded new work', new_work)
            work_uploaded.delay(new_work.id)
            return HttpResponseRedirect('/')
    else:
        form = UploadWorkForm()
        args['form'] = form
        return render_to_response('add_work.html', args, context_instance=RequestContext(request))
