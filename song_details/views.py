from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from file_upload.models import FileModel, CommentModel
from project_manager.models import Project
from project_manager.forms import ProjectAddContributorForm
import os
import base64
from django.conf import settings
import wave
import json
from django.views.generic.base import View
from django.http import HttpResponse
from accounts.models import UserProfile
from django.db.models import Count
from django.contrib.auth.models import User

class TrendingsView(TemplateView):
    template_name = 'song_details/trendings.html'

    def get(self, request, **kwargs):
        most_liked_songs = FileModel.objects.annotate(Count('likes'))[:5]
        most_liked_songs_dict = {}
        audio_files = {}
        user=request.user
        
        for song in most_liked_songs: 
            song_name=song.title
            liked_song=FileModel.objects.filter(title=song_name)[0]
            liked_song_likes=liked_song.likes
            is_already_liked=None
            is_already_liked=liked_song_likes.filter(username=user.username)
            is_already_liked_bool = None
            if is_already_liked.exists():
                is_already_liked_bool = True
            else:
                is_already_liked_bool = False


            current_file_path = str(song.data.name.replace("/","\\"))
            print('-----------'+song.title+"---------"+str(song.total_likes()))
            song_likes={"likes":song.total_likes(),"is_already_liked":is_already_liked_bool}
            print("is_already_liked_bool: "+ str(is_already_liked_bool))
            print(current_file_path)
            current_file_path_length = len(current_file_path)
            current_file_path_wav = str(current_file_path[:current_file_path_length-3] + 'wav')
            print(current_file_path_wav)
            current_file = wave.open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb')
            project_resource_base64=(base64.standard_b64encode(open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb').read())).decode('utf-8')
            audio_files[song.title]=project_resource_base64
            audio_files_as_json=json.loads(json.dumps(audio_files, indent=2))
            commented_song = CommentModel.objects.filter(comments=song)
            if commented_song.exists():
                commented_song=commented_song[0]
                dict_obj={"likes":song.total_likes(),"is_already_liked":is_already_liked_bool, "comments":commented_song.total_comments()}
            else:
                dict_obj={"likes":song.total_likes(),"is_already_liked":is_already_liked_bool}
            print("Likes count:" + str(song.likes__count))
            print("Total likes:" + str(song.total_likes()))
            most_liked_songs_dict[song]=dict_obj

        return render(request, 'song_details/trendings.html', {
            'most_liked_songs': most_liked_songs_dict,
            'audio_files': audio_files,
        })


class SongDetails(TemplateView):
    template_name = 'song_details/song_details.html'

    def get(self, request, **kwargs):
        song_name = kwargs['song_name']
        user=request.user
        authorUsername=kwargs['user_name']
        print("AUTHOR USERNAME = " + authorUsername)
        author=User.objects.filter(username=authorUsername)[0]
        print("AUTHOR ID = " + str(author.id))
        song = FileModel.objects.filter(title=song_name, userProfile_id=author.id)[0]
        print("SONG = " + song.title)
        
        audio_files={}
        song_likes={}

        song_name=song.title
        song_likes=song.likes
        song_comments=CommentModel.objects.filter(comments=song)
        is_already_liked=None

        is_already_liked=song_likes.filter(username=user.username)
        is_already_liked_bool = None
        if is_already_liked.exists():
            is_already_liked_bool = True
        else:
            is_already_liked_bool = False



        current_file_path = str(song.data.name.replace("/","\\"))
        print('!!!-----------!!!'+song.title+"!!!---------!!!"+str(song.total_likes()))
        song_likes={"likes":song.total_likes(),"is_already_liked":is_already_liked_bool}
        print("is_already_liked_bool: "+ str(is_already_liked_bool))
        print(current_file_path)
        current_file_path_length = len(current_file_path)
        current_file_path_wav = str(current_file_path[:current_file_path_length-3] + 'wav')
        print(current_file_path_wav)
        current_file = wave.open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb')
        project_resource_base64=(base64.standard_b64encode(open(os.path.join(settings.BASE_DIR, current_file_path_wav),'rb').read())).decode('utf-8')
        audio_files[song.title]=project_resource_base64
        audio_files_as_json=json.loads(json.dumps(audio_files, indent=2))
        print("SONG LIKES:" + str(song_likes["likes"]))
        print("SONG is_already_liked:" + str(song_likes["is_already_liked"]))

        return render(request, 'song_details/song_details.html', {
            'author_username': authorUsername,
            'song': song,
            'audio_files':audio_files_as_json,
            'song_likes': song_likes,
            'song_comments': song_comments,
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

class CommentView(View):
    def post(self, request, *args, **kwargs):
        user=request.user
        song_name=request.POST.get('song_name')
        print("Song name: " + str(song_name))
        comment_text=request.POST.get('comment_text')
        print("Comment text: " + str(comment_text))
        comment_author=UserProfile.objects.filter(user=user)[0]
        print("Comment author: " + str(comment_author))
        commented_song=FileModel.objects.filter(title=song_name)[0]
        print("Commented song: " + str(commented_song))
        print("AVATAR = " + str(comment_author.avatar))
        comment = CommentModel.objects.create(text=comment_text, author=comment_author)      
        comment.comments.add(commented_song)
        comment.save()
        #is_already_liked=liked_song.filter(likes=user)
        #print(is_already_liked)
        ctx = {
                    'is_already_liked' : True,   
                }

        return HttpResponse(json.dumps(ctx), content_type='application/json')