from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.generic import TemplateView
from .models import FileModel
from django.core.exceptions import ValidationError

# Imaginary function to handle an uploaded file.
#from .file_upload_utilities import handle_uploaded_file

class UploadFile(TemplateView):
    template_name = 'file_upload/upload.html'
    def post(self, request, **kwargs):
        print('v posta sum')
        form = UploadFileForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()

            #instance = FileModel(data=request.FILES['file'])
            #instance.save()
            
                form.save()
                print('tashachki')
        
            #return HttpResponseRedirect('/success/url/')
            return render(request, 'file_upload/upload.html', {'form': form})
        except Exception as e:
            print('cicki')
            return render(request, 'file_upload/upload.html', {'form': form})

            
        
    def get(self, request, **kwargs):
        print('v geta sym')
        form = UploadFileForm()
        return render(request, 'file_upload/upload.html', {'form': form})
    