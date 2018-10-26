from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView
from django.views.generic.base import View

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

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['loggedIn'] = False
        if self.request.user.is_authenticated:
            ctx['loggedIn'] = True
        return ctx


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

            return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
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
                return redirect('/')
            else:
                return HttpResponse('Error: User authentication error <a href="/login"">Try again</a>')
        else:
            return HttpResponse('Error: Username or password is empty <a href="/login">Try again</a>')


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('/')
