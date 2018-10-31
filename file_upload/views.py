from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.generic import TemplateView
from .models import FileModel
from django.core.exceptions import ValidationError
from project_manager.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin

# Imaginary function to handle an uploaded file.
#from .file_upload_utilities import handle_uploaded_file

class UploadFile(LoginRequiredMixin, TemplateView):
    template_name = 'file_upload/upload.html'
    
    def post(self, request, **kwargs):
        print('v posta sum na uploadFile')
        form = UploadFileForm(request.POST, request.FILES)
        print(form.is_valid())
        try:
            if form.is_valid():
                #username=request.user.username
                afile=request.FILES['data']
                file_name=request.POST['title']
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
                    file_model.data.field.upload_to = 'user_projects/'+username+'/'+project_name+'/'
                    project=Project.objects.filter(name=project_name)[0]
                    file_model.project=project
                else:
                    file_model.data.field.upload_to = 'user_projects/'+username+'/'
                file_model.userProfile=current_user
                form.save()
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
