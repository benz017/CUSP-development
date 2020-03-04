from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.landing, name='index'),
    path('success', views.success, name='subscribe'),
    path('pay', views.pay, name='payment'),
    path('events', views.events, name='404'),
    path('products', views.products, name='404'),
    path('blogs', views.blogs, name='404'),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)