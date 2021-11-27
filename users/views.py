import re
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import custom_user_creation_form,edit_account_form, message_form,skill_form
from .models import Profile,Skill,Messages
from .utils import search_profile,paginate_profiles

# Create your views here.
def profiles(request):
    profiles,search_query=search_profile(request)

    context2,profiles=paginate_profiles(request,profiles)

    context={'profiles':profiles,'search_query':search_query,
             'page_num_range':context2['page_num_range'],'current_page_num':context2['current_page_num'],
             'is_having_previous_page':context2['is_having_previous_page'],'is_having_next_page':context2['is_having_next_page'],
             'previous_page_number':context2['previous_page_number'],'next_page_number':context2['next_page_number'],
             'is_having_other_pages':context2['is_having_other_pages'],'custom_page_num_range':context2['custom_page_num_range'],
             'last_page_num':context2['last_page_num'],'last_page_num_minus_1':context2['last_page_num_minus_1']
             }
    return render(request,'users/profiles.html',context)

def user_profile(request,pk):
    profile=Profile.objects.get(id=pk)
    top_skills=profile.skill_set.exclude(description__exact="")
    other_skills=profile.skill_set.filter(description="")
    context={'profile':profile,'top_skills':top_skills,'other_skills':other_skills}
    return render(request,'users/user-profile.html',context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles') 

    if request.method=='POST':
        entered_username=request.POST['username']
        entered_password=request.POST['password']
        try:
            user=User.objects.get(username=entered_username)
        except:
            messages.error(request,'Username does not exists')
        user=authenticate(request,username=entered_username,password=entered_password)

        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            messages.error(request,'Username or Password is incorrect')

    page='login'
    context={'page':page}
    return render(request,'users/login_signup.html',context)

def logout_user(request):
    logout(request)
    messages.success(request,'User was logged out!')
    return redirect('login')

def signup(request):
    page='signup'
    form=custom_user_creation_form()
    if request.method=='POST':
        form=custom_user_creation_form(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'User was created successfully')
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,'something went wrong')

            
    context={'page':page,'form':form}
    return render(request,'users/login_signup.html',context)

@login_required(login_url='login')
def my_account(request):
    my_profile=request.user.profile
    skills=my_profile.skill_set.all()
    projects=my_profile.project_set.all()
    context={'my_profile':my_profile,'skills':skills,'projects':projects}
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def edit_account(request):
    profile_data=request.user.profile
    form=edit_account_form(instance=profile_data)
    if request.method=='POST':
        form=edit_account_form(request.POST,request.FILES,instance=profile_data)
        if form.is_valid():
            form.save()
            return redirect('my-account')
    context={'form':form}
    return render(request,'users/edit_my_account.html',context)

@login_required(login_url='login')
def create_skill(request):
    profile=request.user.profile
    form=skill_form()
    if request.method=='POST':
        form=skill_form(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill was added successfully!')
            return redirect('my-account')

    context={'form':form}
    return render(request,'users/skill-form.html',context)

@login_required(login_url='login')
def update_skill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=skill_form(instance=skill)
    if request.method=='POST':
        form=skill_form(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was Updated successfully!')
            return redirect('my-account')

    context={'form':form}
    return render(request,'users/skill-form.html',context)

@login_required(login_url='login')
def delete_skill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method=='POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('my-account')
    context={'object':skill}
    return render(request,'delete_template.html',context)

@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    message_requests=profile.recievedmessages.all()
    unread_count=message_requests.filter(is_read=False).count()
    context={'message_requests':message_requests,'unread_count':unread_count}
    return render(request,'users/inbox.html',context)


@login_required(login_url='login')
def view_message(request,pk):
    profile=request.user.profile
    message=profile.recievedmessages.get(id=pk)

    if message.is_read==False:
        message.is_read=True
        message.save()

    context={'message':message}
    return render(request,'users/message.html',context)

@login_required(login_url='login')
def send_message(request,pk):
    recipient=Profile.objects.get(id=pk)
    sender=request.user.profile
    if recipient != sender:
        form=message_form()
        if request.method=='POST':
            form=message_form(request.POST)
            if form.is_valid():
                message=form.save(commit=False)
                message.sender=sender
                message.recipient=recipient
                message.save()
                messages.success(request,'Message sent successfullyy')
                return redirect('user-profile',pk=recipient.id)

        context={'recipient':recipient,'form':form}
        return render(request,'users/message_form.html',context)
    else:
        messages.error(request,'You cannot send message to yourself')
        return redirect('user-profile',pk=recipient.id)