from django.urls import path

from . import views

app_name = 'project_manager'

urlpatterns = [
    path('projects/<str:user_name>/', views.ProjectsListView.as_view(), name='projects'),
    path('projects/<str:user_name>/<str:project_name>/', views.ProjectDetailView.as_view(), name='projectDetails'),
    path('add_project/', views.AddProjectView.as_view(), name='add_project'),
]
