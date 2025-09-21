from django.urls import path
from airwrite.interfaces.django_views.home import ModuleListView
from airwrite.interfaces.django_views.trazos import index, video_feed_cam, video_feed_canvas

urlpatterns = [
    # Rutas actuales
    path('', ModuleListView.as_view(), name='home'),
    path('trazos/', index, name='trazos'),
    path('video/cam/', video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', video_feed_canvas, name='video_feed_canvas'),

    # Alias legacy para compatibilidad con rutas antiguas
    path('core/trazos/', index, name='trazos_legacy'),
    path('core/video/cam/', video_feed_cam, name='video_feed_cam_legacy'),
    path('core/video/canvas/', video_feed_canvas, name='video_feed_canvas_legacy'),
]