"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
the include and routers its special for the viewsets
rest framework method
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tickets import views

router = routers.DefaultRouter()
router.register('guests' , views.viewsets_guest)
router.register('movies' , views.viewsets_movie)
router.register('reservation' , views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('no_rest_yes_model', views.no_rest_yes_model),
    path('fbv_list', views.fbv_list),
    path('fbv_pk/<int:pk>', views.fbv_pk),
    path('cbv_list', views.cbv_list.as_view()),
    path('cbv_pk/<int:pk>', views.cbv_pk.as_view()),
    path('cbv_mx', views.cbv_mx.as_view()),
    path('cbv_mx_pk/<int:pk>', views.cbv_mx_pk.as_view()),
    path('gen', views.gen.as_view()),
    path('gen_pk/<int:pk>', views.gen_pk.as_view()),
    path('viewsets/', include(router.urls)),

]
