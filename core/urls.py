# DEPRECATED: Rutas migradas a airwrite.interfaces.django_views.urls_core
# Se mantiene para compatibilidad, pero ahora delega vistas en airwrite
from django.urls import path
from airwrite.interfaces.django_views.home import ModuleListView
from airwrite.interfaces.django_views.trazos import video_feed_cam, video_feed_canvas, index

urlpatterns = [
    path('', ModuleListView.as_view(), name='home'),
    path('core/trazos/', index, name='trazos'),
    path('video/cam/', video_feed_cam, name='video_feed_cam'),
    path('video/canvas/', video_feed_canvas, name='video_feed_canvas'),
]
