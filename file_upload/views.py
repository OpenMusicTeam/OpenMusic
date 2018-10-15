from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.generic import TemplateView
from .models import FileModel

# Imaginary function to handle an uploaded file.
#from .file_upload_utilities import handle_uploaded_file

class UploadFile(TemplateView):
    template_name = 'file_upload/upload.html'
    def post(self, request, **kwargs):
        print('v posta sum')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #instance = FileModel(data=request.FILES['file'])
            #instance.save()
            form.save()
            #return HttpResponseRedirect('/success/url/')
            return render(request, 'file_upload/upload.html', {'form': form})

            
        
    def get(self, request, **kwargs):
        print('v geta sym')
        form = UploadFileForm()
        return render(request, 'file_upload/upload.html', {'form': form})
    