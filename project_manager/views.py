from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm

class ProjectDetailView(DetailView):
    template_name = 'project_manager/project_details.html'

    def get(self, request, **kwargs):
        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        #project = Project.objects.all()[0]

        print(project != None)
        print(project)
        return render(request, 'project_manager/project_details.html', {
            'project': project,
        })

class ProjectsListView(ListView):
    template_name = 'project_manager/project_list.html'

    def get(self, request, **kwargs):
        username = kwargs['user_name']
        user_id = User.objects.get(username=username).pk
        all_projects_list = Project.objects.filter(userProfile__exact=user_id)
        return render(request, 'project_manager/project_list.html', {
            'project_set': all_projects_list,
            'username': username,
            'user_id': user_id,
        })

class AddProjectView(TemplateView):
    template_name = 'project_manager/add_project.html'

    def get_context_data(self, **kwargs):
        ctx = super(AddProjectView, self).get_context_data(**kwargs)
        ctx['project_form'] = ProjectForm()
        print("in get_context_data function")
        return ctx

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        print("in post method")
        print(project_form.is_valid())
        print(project_form)
        if(project_form.is_valid()):
            current_user=request.user
            project = project_form.save(commit=False)   
            project.userProfile=current_user
            project.save()
            print("ProjectsListView in IF")
            return HttpResponse("Project added  !<br><a href='/'>Go to home</a>")  
        else:
            print("ProjectsListView in ELSE")
            return render(request, 'project_manager/project_list.html',{'project_form':project_form,})
