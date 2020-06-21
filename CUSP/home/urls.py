from django.urls import path
from django.conf import settings
from django.shortcuts import redirect
from django.conf.urls.static import static
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.landing, name='index'),
    path('success', views.sub_success, name='subscribe'),
    path('events', views.events, name='404'),
    path('products', views.products, name='404'),
    path('blogs', views.blogs, name='404'),
    path('accounts/dashboard', views.account, name='account'),
    path('accounts/my-orders', views.myorders, name='orders'),
    path('accounts/my-calender', views.mycalender, name='calender'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/signin', views.signin, name='signin'),
    path('accounts/signout', views.signout, name='signout'),
    path(r'accounts/social/login/cancelled/', views.login_cancelled, name="login_cancelled"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
