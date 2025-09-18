from django.urls import path
from core.views.home import ModuleListView
from core.views.trazos import video_feed_cam, video_feed_canvas, index
from airwrite.interfaces.django_views.trazos import recognize_canvas_text


urlpatterns = [
    path('', ModuleListView.as_view(), name='home'),
    path('core/trazos/', index, name='trazos'),
    path('video/cam/', video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', video_feed_canvas, name='video_feed_canvas'),
    path('api/ocr-canvas/', recognize_canvas_text, name='ocr_canvas'),
]
