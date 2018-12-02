
from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

app_name = 'file_upload'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/file_upload/upload'), name='index'),
    url(r'^upload/$', views.UploadFile.as_view(), name='upload'),
]
