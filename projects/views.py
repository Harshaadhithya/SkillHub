from django import forms
from django.core import paginator
from django.shortcuts import render,redirect
from .models import Project, Review, Tag
from .forms import ProjectFrom,Review_form
from django.contrib.auth.decorators import login_required
from .utils import search_projects,paginate_projects
from django.contrib import messages

from users.models import Profile




# Create your views here.
def projects(request):
    projectsList,search_query=search_projects(request)

    context2,projectsList=paginate_projects(request,projectsList)
    
    context={'projectsList':projectsList,'search_query':search_query,
             'page_num_range':context2['page_num_range'],'current_page_num':context2['current_page_num'],
             'is_having_previous_page':context2['is_having_previous_page'],'is_having_next_page':context2['is_having_next_page'],
             'previous_page_number':context2['previous_page_number'],'next_page_number':context2['next_page_number'],
             'is_having_other_pages':context2['is_having_other_pages'],'custom_page_num_range':context2['custom_page_num_range'],
             'last_page_num':context2['last_page_num'],'last_page_num_minus_1':context2['last_page_num_minus_1']
             }
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    tags=projectObj.tags.all()
    form=Review_form()
 
    project_owner=projectObj.owner.id
    if request.user.is_authenticated:
        reviewer_id=request.user.profile.id
        if project_owner==reviewer_id:    
            is_own_project=True
        else:
            is_own_project=False
    else:
        reviewer_id=None
        is_own_project=None

    checking_already_exist=projectObj.review_set.filter(owner__id=reviewer_id)
    if checking_already_exist:
        print(checking_already_exist)
        is_already_voted=True    
    else:
        is_already_voted=False
        
    if not is_own_project:
        if request.method=='POST':
            form=Review_form(request.POST)
            review=form.save(commit=False)
            review.owner=request.user.profile
            review.project=projectObj
            review.save()

            projectObj.count_vote

            messages.success(request,'Your review was added successfully!')
            return redirect('project',pk=projectObj.id)
        
    context={'project':projectObj,'tags':tags,'form':form,'is_own_project':is_own_project,'is_already_voted':is_already_voted}
    return render(request,'projects/single-project.html',context)

@login_required(login_url='login')
def create_project(request):
    profile=request.user.profile
    form=ProjectFrom()
    if request.method=='POST':
        newtags=request.POST['newtags'].replace(","," ").split()

        form=ProjectFrom(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()

            for entered_tag in newtags:
                tag,created=Tag.objects.get_or_create(name=entered_tag)
                project.tags.add(tag)

            return redirect('my-account')
    context={'form':form}
    return render(request,'projects/form_template.html',context)

@login_required(login_url='login')
def update_project(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectFrom(instance=project)
    if request.method=='POST':
        newtags=request.POST['newtags'].replace(","," ").split()
        form=ProjectFrom(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project=form.save()
            for entered_tag in newtags:
                tag,created=Tag.objects.get_or_create(name=entered_tag)
                project.tags.add(tag)
            return redirect('my-account')
    context={'form':form,'project':project}
    return render(request,'projects/form_template.html',context)


@login_required(login_url='login')
def delete_project(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method=='POST':
        project.delete()
        return redirect('my-account')
    context={'object':project.title}
    return render(request,'delete_template.html',context)

