from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.base import View
import base64
from .models import UserProfile,User
from django.conf import settings
import wave
import json
from file_upload.models import FileModel
from .forms import ProfileForm
from .forms import UserForm
import os


# @receiver(post_save, sender=User)
# def create_profile(sender, instance , created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance , **kwargs):
#     print(dir(instance))
#     instance.userprofile.save()

class ProfileView(TemplateView):
    template_name = 'profile.html'
    
    def get(self, request, **kwargs):
        username = kwargs['username']
        user = User.objects.filter(username=username)[0]
        userProfile = UserProfile.objects.filter(user=user)[0]

        return render(request, 'profile.html', {
            'userProfile': userProfile
        })   

class Index(TemplateView):
    template_name = 'index.html'
    def get(self,request, **kwargs):
        user=request.user
        published_projects = FileModel.objects.filter(project_publish_resource_id__isnull=False)

        for resource in published_projects:
            if resource.title == "Jazz":
                print(resource.title + " 1010010101010")
                print(resource.total_likes())
                print(resource.description)

        ready_songs = FileModel.objects.filter(project_id__isnull=True)
        print(ready_songs)
        """user=request.user
        song_name=request.POST.get('song_name')
        liked_song=FileModel.objects.filter(title=song_name)[0]
        liked_song_likes=liked_song.likes
        is_already_liked=None
        print("(BEFORE) IS ALREADY LIKED: " + str(is_already_liked))
        is_already_liked=liked_song_likes.filter(username=user.username)
        is_already_liked_bool = None
        if is_already_liked.exists():
            is_already_liked_bool = True
        else:
            is_already_liked_bool = False"""
        songs_to_iterate = published_projects | ready_songs
        audio_files={}
        songs_and_likes={}
        for current_project_resource in songs_to_iterate :
            song_name=current_project_resource.title
            liked_song=FileModel.objects.filter(title=song_name)[0]
            liked_song_likes=liked_song.likes
            is_already_liked=None
            print("(BEFORE) IS ALREADY LIKED: " + str(is_already_liked))
            is_already_liked=liked_song_likes.filter(username=user.username)
            is_already_liked_bool = None
            if is_already_liked.exists():
                is_already_liked_bool = True
            else:
                is_already_liked_bool = False

            author_id = current_project_resource.userProfile_id
            author_username = User.objects.filter(id=author_id)[0]
            current_file_path = str(current_project_resource.data.name.replace("/","\\"))
            current_project_image_url=current_project_resource.project_publish_image_url
            current_project_genre=current_project_resource.genre
            print('-----------'+current_project_resource.title+"---------"+str(current_project_resource.total_likes())+"--------------------"+str(author_username))
            songs_and_likes[current_project_resource]={"likes":current_project_resource.total_likes(),"is_already_liked":is_already_liked_bool, 'author_username': author_username, "image":current_project_image_url, "genre":current_project_genre}
            print(current_file_path)
            current_file_path_length = len(current_file_path)
            current_file_path_wav = str(current_file_path[:current_file_path_length-3] + 'wav')
            print(current_file_path_wav)
            current_file = wave.open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb')
            project_resource_base64=(base64.standard_b64encode(open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb').read())).decode('utf-8')
            audio_files[current_project_resource.title]=project_resource_base64
        audio_files_as_json=json.loads(json.dumps(audio_files, indent=2))

        return render(request, 'index.html', {
            'published_projects': songs_to_iterate,
            'audio_files':audio_files_as_json,
            'songs_and_likes': songs_and_likes,
        })

class LikeView(View):
    def post(self, request, *args, **kwargs):
        user=request.user
        song_name=request.POST.get('song_name')
        print("SONG_NAME = " + song_name)
        song_author_username=request.POST.get('song_author')
        print("SONG_AUTHOR_USERNAME = " + song_author_username)
        author = User.objects.filter(username=song_author_username)[0]
        author_id = author.id
        liked_song=FileModel.objects.filter(title=song_name, userProfile_id=author_id)[0]
        liked_song_likes=liked_song.likes
        print("LIKED_SONG_LIKES = " + str(liked_song_likes))
        is_already_liked=None
        print("(BEFORE) IS ALREADY LIKED: " + str(is_already_liked))
        is_already_liked=liked_song_likes.filter(username=user.username)
        if is_already_liked.exists():
            print("IS ALREADY LIKED: " + str(is_already_liked[0]))
            ctx = {
                    'likes_count': liked_song.total_likes(),
                    'is_already_liked' : False,
                }
            liked_song.likes.remove(user)
        else:
            ctx = {
                    'likes_count': liked_song.total_likes(),
                    'is_already_liked' : True,
                   
                }
            liked_song.likes.add(user)    
        #is_already_liked=liked_song.filter(likes=user)
        #print(is_already_liked)
        
        
        return HttpResponse(json.dumps(ctx), content_type='application/json')

class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        ctx = super(SignUpView, self).get_context_data(**kwargs)
        ctx['user_form'] = UserForm(prefix='user')
        ctx['profile_form'] = ProfileForm(prefix='profile')
        return ctx

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, prefix='user')
        profile_form = ProfileForm(request.POST, request.FILES, prefix='profile')
        print(profile_form.is_valid())
        print(user_form.is_valid())
        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()

            folderPath = './user_projects/' + user.username
            self.createFolder(folderPath)

            return render(request, 'index.html',{'message':"Account created successfully."})
            #return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
        else:           
            #return redirect('/accounts/signup/', {'errorMessage': 'This username or email is already in use!',})
            return render(request, 'signup.html',{'user_form':user_form, 'profile_form': profile_form,})

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)

class LoginView(TemplateView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                valuenext= request.POST['next']
                if valuenext is not None and valuenext is not '':
                    return redirect(valuenext)
                else: 
                    return redirect('/')
            else:
                return render(request, 'registration/login.html', {
                    'message': "Incorrect username or password"
                })
        else:
            return render(request, 'registration/login.html', {
                'message': "Username or password are empty"
            })


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('/')