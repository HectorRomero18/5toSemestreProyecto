from django.urls import path
from core.views.home import ModuleListView
from core.views.trazos import video_feed_cam, video_feed_canvas, index


urlpatterns = [
    path('', ModuleListView.as_view(), name='home'),
    path('core/trazos/',index , name='trazos'),
    path('video/cam/', video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', video_feed_canvas, name='video_feed_canvas'),
]
