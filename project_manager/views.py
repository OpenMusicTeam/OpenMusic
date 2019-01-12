from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect
from .models import Project
from django.contrib.auth.models import User
from .forms import ProjectForm
from .forms import ProjectForm, ProjectAddContributorForm
from file_upload.forms import UploadFileForm
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from file_upload.models import FileModel
from django.conf import settings
from accounts.forms import UserForm, ProfileForm
import base64
import sys
import json
from .forms import ProjectPublishForm
from django.utils.safestring import mark_safe
import wave
import re
#import pathlib
from scipy.io import wavfile as wav
from .audio_analysis import Make_Audio_Analysis

class SoundAnalysisView(LoginRequiredMixin, DetailView):
    template_name = 'project_manager/sound_analysis.html'


    def post(self, request, **kwargs):
        username = kwargs['user_name']
        currently_logged_username=request.user.username
        if username!=currently_logged_username:
            url='/project_manager/projects/'+currently_logged_username+'/'
            return redirect(url)

        checked_songs = request.POST.getlist('checkedSongs')
        song1_title=checked_songs[0].split("/")[0]
        song2_title=checked_songs[1].split("/")[0]
        song1_data=checked_songs[0].split("/")[1]
        song2_data=checked_songs[1].split("/")[1]
        print("Checked songs:")
        print(checked_songs)
        #project_name = self.kwargs['project_name']
        #json_fig = self.make_graph(song_name, username, project_name)
        project_name = self.kwargs['project_name']
        json_figs_list = Make_Audio_Analysis(song1_data, song2_data, username, project_name)
        #Make_Audio_Analysis(song1_data, song2_data, username, project_name)
        print("Analysis ended.")
        json_fig1 = json_figs_list[0]
        json_fig2 = json_figs_list[1]
        volume_percent = json_figs_list[2]
        return render(request, 'project_manager/sound_analysis.html', {
            'song1_title': song1_title,
            'song2_title': song2_title,
            'json_fig1': json_fig1,
            'json_fig2': json_fig2,
            'volume_percent': volume_percent,
        })


class EditResourcesView(LoginRequiredMixin, TemplateView):
    template_name = 'project_manager/edit_resources.html'

    def encode_audio(self):
        audio_content = audio.read()
        return base64.b64encode(audio_content)

    def get(self, request, **kwargs):
        username = kwargs['user_name']
        currently_logged_username=request.user.username
        if username!=currently_logged_username:
            url='/project_manager/projects/'+currently_logged_username+'/'
            return redirect(url)

        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        project_id = project.id
        user_id = request.user.id
        project_resources = FileModel.objects.filter(project_id=project_id)
        audio_files={}

        for current_project_resource in project_resources :
            
            current_file_path = str(current_project_resource.data.name.replace("/","\\"))
            print(current_file_path)
            current_file_path_length = len(current_file_path)
            print(current_file_path_length)
            current_file_path_wav = str(current_file_path[:current_file_path_length-3] + 'wav')
            print(current_file_path_wav)
            current_file = wave.open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb')
            '''encoded_audio = base64.b64encode(audio_file)
            print(encoded_audio)
            project_resources_filedata_base64=encoded_audio'''

            project_resource_base64=(base64.standard_b64encode(open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb').read())).decode('utf-8')
            #print("ReSOURCE TITLE = " + current_project_resource.title)
            #project_resource_string= [t.encode('utf-8') for t in title]
            audio_files[current_project_resource.title]=project_resource_base64
        print("======================= Files ===========================================")
        #print(audio_files.keys())
        
        audio_files_as_json=json.loads(json.dumps(audio_files, indent=2))
        #print(audio_files_as_json)
        dictionary = {
            'int': 2,
            'str': "a",
            'float': 0.2
        }
        dictionary['aaa']=5
        dict_as_json=json.loads(json.dumps(dictionary))
        #print(dictionary)

        #project = Project.objects.all()[0]
        return render(request, 'project_manager/edit_resources.html', {
            'project_resources': project_resources,
            'audio_files':audio_files_as_json,
        })

    def post(self, request, *args, **kwargs):
        print("in post method")       
 


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

        project_resources_formated_data=[]
        for resource in project_resources:
           new_data = re.search('[^/]+$', str(resource.data)).group(0)
           resource.data = new_data
           project_resources_formated_data.append(resource)
        print("======================= Files ===========================================")
        previous_url = request.path
        print(project_resources)
        #project = Project.objects.all()[0]

        print(project != None)
        print(project)
        form=ProjectAddContributorForm()
        return render(request, 'project_manager/project_details.html', {
            'project': project,
            'project_resources': project_resources_formated_data,
            'form': form,
            'previous_url': previous_url
        })
    def post(self, request, *args, **kwargs):
        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        addContributorForm=ProjectAddContributorForm(request.POST)
        print('--------------------------------')
        print(addContributorForm.is_valid())
        if(addContributorForm.is_valid()):
            added_contributor=addContributorForm.cleaned_data['contributors'][0]
            new_form=ProjectAddContributorForm()
            print('========================')
            print(project.contributors)
            project.contributors.add(added_contributor)
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


class ProjectPublishView(LoginRequiredMixin, DetailView):
    def get(self, request, **kwargs):
        username = kwargs['user_name']
        currently_logged_username=request.user.username
        if username!=currently_logged_username:
            url='/project_manager/projects/'+currently_logged_username+'/'
            return redirect(url)

        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        project_id = project.id
        project_resources = FileModel.objects.filter(project_id=project_id)
        return render(request, 'project_manager/project_publish.html', {
            'project': project,
            'project_resources': project_resources,
        })

    def post(self, request, *args, **kwargs):
        currently_logged_username=request.user.username
        publish_value=request.POST.get('rate')
        selected_genre=request.POST.get('projectGenre')
        project_image_url=request.POST.get('project_image_url')
        if(len(project_image_url) == 0):
            project_image_url = "https://res.cloudinary.com/easymedicine/image/upload/DefaultSongImage.png"
        print('??????????'+project_image_url)
        project = Project.objects.filter(name__exact=self.kwargs['project_name'])[0]
        project_publish_resource = FileModel.objects.filter(title=publish_value)[0]
        project_publish_resource.project_publish_resource=project
        project_publish_resource.genre=selected_genre
        project_publish_resource.project_publish_image_url=project_image_url
        project_publish_resource.save()
        print("--------------"+publish_value)
        url='/project_manager/projects/'+currently_logged_username+'/'+project.name+'/'
        return redirect(url)


class ProjectsListView(LoginRequiredMixin, ListView):
    template_name = 'project_manager/project_list.html'

    def ctx(self):
        ctx = {}
        ctx['loggedIn'] = False
        print("User is authenticated = " + self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            ctx['loggedIn'] = True
        return ctx

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
            #print(all_projects_list)

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
                project_path='/OpenMusicOfficial/OpenMusic_current/user_projects/'+username+'/'+project.name

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
