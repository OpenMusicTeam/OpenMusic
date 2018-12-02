from django.urls import path

from . import views

app_name = 'song_details'

urlpatterns = [
    path('details/<str:song_name>/', views.SongDetails.as_view(), name='details'),
    path('trendings/', views.TrendingsView.as_view(), name='trendings'),
    path('like/', views.LikeView.as_view(), name='like'),
    path('comment/', views.CommentView.as_view(), name='comment'),
]