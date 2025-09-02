from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('video/cam/', views.video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', views.video_feed_canvas, name='video_feed_canvas'),
]
