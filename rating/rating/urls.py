from django.contrib import admin
from django.urls import path

from rating import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get/listModule',views.ModuleList.as_view()),
    path('get/logout',views.Logout.as_view()),
    path('get/view',views.View.as_view()),
    path('get/login',views.Login.as_view()),
    path('get/average',views.Average.as_view()),
    path('post/register',views.Register.as_view()),
    path('post/rate',views.RateProcess.as_view()),
]
