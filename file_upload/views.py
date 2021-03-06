from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.generic import TemplateView
from .models import FileModel
from django.core.exceptions import ValidationError
from project_manager.models import Project
from pydub import AudioSegment
import pydub
import re
from django.contrib.auth.mixins import LoginRequiredMixin

# Imaginary function to handle an uploaded file.
#from .file_upload_utilities import handle_uploaded_file

class UploadFile(LoginRequiredMixin, TemplateView):
    template_name = 'file_upload/upload.html'
    pydub.AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
    def post(self, request, **kwargs):
        print('v posta sum na uploadFile')
        form = UploadFileForm(request.POST, request.FILES)
        print(form.is_valid())
        try:
            if form.is_valid():
                print("form is validddddd")
                #username=request.user.username
                afile=request.FILES['data']
                file_name=request.POST['title']
                
                #isAnEditedSong=request.POST['isAnEditedSong']
                isAnEditedSong=request.POST.get('isAnEditedSong', '') == True
                current_user=request.user
                username=request.user.username
                print(file_name)                
                print(afile)
                #file_model=FileModel(title=file_name,data=afile)
                file_model = form.save(commit=False)
                print(1)
                

                #instance = FileModel(data=request.FILES['file'])
                #instance.save()
                project_name=request.POST['project_name']
                print('Project_name = ' + project_name)
                if project_name is not None and project_name is not '':
                    #file_model.data.field.upload_to = 'user_projects/'+username+'/'+project_name+'/'
                    file_model.data.field.upload_to = 'project_manager/static/user_projects/'+username+'/'+project_name+'/'
                    project=Project.objects.filter(name=project_name)[0]
                    file_model.project=project
                else:
                    #file_model.data.field.upload_to = 'user_projects/'+username+'/'
                    file_model.data.field.upload_to = 'project_manager/static/user_projects/'+username+'/'
                file_model.userProfile=current_user
                form.save()
                file_path = str(file_model.data)
                file_path_length=len(file_path)
                print('before search')
                #file_extension = re.search('\.[^.]*?$', file_path)
                file_extension = file_path[-3:]
                print(file_extension)
                print('after search')
                if file_extension == "mp3":
                    print(file_path)
                    new_path = file_path[:file_path_length-3] + 'wav'
                    print(new_path)
                    AudioSegment.from_mp3(file_path).export(new_path, format="wav")
                print('In the try')
        
            return render(request, 'file_upload/upload.html', {'form': form})
        except Exception as e:
            print('In the catch')
            print(e)
            return render(request, 'file_upload/upload.html', {'form': form})

            
        
    def get(self, request, **kwargs):
        print('v geta sym')
        form = UploadFileForm()
        return render(request, 'file_upload/upload.html', {'form': form})
