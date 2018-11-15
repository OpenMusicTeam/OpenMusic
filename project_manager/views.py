from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm, ProjectAddContributorForm
from file_upload.forms import UploadFileForm
from accounts.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from file_upload.models import FileModel
import os
#import pathlib

class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = 'project_manager/project_details.html'

    def get(self, request, **kwargs):
        username = kwargs['user_name']
        currently_logged_username=request.user.username
        if username!=currently_logged_username:
            url='/project_manager/projects/'+currently_logged_username+'/'
            return redirect(url)

        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        project_id = project.id
        project_resources = FileModel.objects.filter(project_id=project_id)
        print("======================= Files ===========================================")
        previous_url = request.path
        print(project_resources)
        #project = Project.objects.all()[0]

        print(project != None)
        print(project)
        form=ProjectAddContributorForm()
        return render(request, 'project_manager/project_details.html', {
            'project': project,
            'project_resources': project_resources,
            'form': form,
            'previous_url': previous_url
        })
    def post(self, request, *args, **kwargs):
        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        addContributorForm=ProjectAddContributorForm(request.POST)
        print('--------------------------------')
        print(addContributorForm.is_valid())
        if(addContributorForm.is_valid()):
            added_contributor=addContributorForm.cleaned_data['contributor'][0]
            new_form=ProjectAddContributorForm()
            print('========================')
            print(project.contributor)
            project.contributor.add(added_contributor)
            return render(request, 'project_manager/project_details.html', {
            'project': project,
            'form': new_form,
        })
        else:
            form=UploadFileForm()
            return render(request, 'file_upload/upload.html', {
                'project_name': project.name,
                'form': form,
            })

class ProjectsListView(LoginRequiredMixin, ListView):
    template_name = 'project_manager/project_list.html'

    def get(self, request, **kwargs):
        username = kwargs['user_name']
        currently_logged_username=request.user.username
        user_id = User.objects.get(username=currently_logged_username).pk
        all_projects_list = list(Project.objects.filter(userProfile__exact=user_id))
        all_contributed_projects=list(Project.objects.filter(contributors__user__id=request.user.id))
        if  len(all_contributed_projects)>0:
            all_projects_list.extend(all_contributed_projects)

        if username!=currently_logged_username:
            url='/project_manager/projects/'+currently_logged_username+'/'
            return redirect(url)
        
        else:
            print(all_projects_list)

            if 'message' in request.session:
                message = request.session['message']
                del request.session['message']
                context = {
                    'project_set': all_projects_list,
                    'username': username,
                    'user_id': user_id,
                    'message': message,
                }
            else:
                context = {
                    'project_set': all_projects_list,
                    'username': username,
                    'user_id': user_id,
                }
            
            return render(request, 'project_manager/project_list.html', context)


class AddProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'project_manager/add_project.html'

    def get(self, request, **kwargs):
        project_form = ProjectForm()
        return render(request, 'project_manager/add_project.html', {'project_form': project_form})

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        print("in post method")
        print(project_form.is_valid())
        if(project_form.is_valid()):
            project_name=project_form.cleaned_data['name']
            user=request.user
            user_projects = Project.objects.filter(userProfile=user)
            if user_projects.filter(name=project_name).exists():
                message="A project with that name already exists."
                project_form = ProjectForm()
                return render(request, 'project_manager/add_project.html', {
                    'message': message,
                    'project_form': project_form,
                })
            else:
                current_user=request.user
                username=current_user.username
                project = project_form.save(commit=False)  
                project_path='/OpenMusicOfficial/OpenMusic/user_projects/'+username+'/'+project.name

                """pathlib.Path(project_path).mkdir(parents=True, exist_ok=True)"""
                try:
                    print("in the try")
                    if not os.path.exists(project_path):
                        os.mkdir(project_path)
                except OSError:
                    sys.exit('Fatal: output directory "' + project_path + '" does not exist and cannot be created')
                
                project.userProfile=current_user
                project.save()
                print("ProjectsListView in IF")
                
                message="Project added successfully"
                request.session['message']=message
                url='/project_manager/projects/'+username+'/'
                return redirect(url)

                #return HttpResponse("Project added  !<br><a href='/'>Go to home</a>")  
        else:
            print("ProjectsListView in ELSE")
            project_form=ProjectForm()
            return render(request, 'project_manager/project_list.html',{'project_form':project_form})
