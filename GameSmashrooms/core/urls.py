from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .views import rechazar_noticia
from .views import actualizar_plan
from .views import voucher
from rest_framework import routers
from .views import PeriodistaViewSet, NoticiaViewSet 
from django.contrib.auth import views as auth_views




routers = routers.DefaultRouter()
routers.register('periodistas',PeriodistaViewSet)
routers.register('noticia',NoticiaViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    path('base/', views.base, name="base"),
    path('periodistas/', views.periodistas, name="periodistas"),
    path('categori/', views.categori, name="categori"),
    path('contacto/', views.contacto, name="contacto"),
    path('latest_news/', views.latest_news, name="latest_news"),
    path('internacionales/', views.Internacionales, name="internacionales"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('noticia/<int:noticia_id>/', views.noticia, name='noticia'),
    path('noticia_add/', views.noticia_add, name='noticia_add'),
    path('editar_noticia/<int:noticia_id>/', views.editar_noticia, name='editar_noticia'),
    path('noticia_delete/<int:noticia_id>/', views.noticia_delete, name="noticia_delete"),
    path('register/', views.register, name="register"),
    path('miperfil/', views.miperfil, name="miperfil"),
    path('crear_periodista/', views.crear_periodista, name="crear_periodista"),
    path('admin2/', views.admin2, name="admin2"),
    path('noticia_admin/', views.noticia_admin, name="noticia_admin"),
    path('lista_admin/', views.lista_admin, name="lista_admin"),
    path('aprobar/<int:noticia_id>/', views.aprobar_noticia, name='aprobado'),
    path('rechazar_noticia/', views.rechazar_noticia, name='rechazar_noticia'),
    path('suscripcion/', views.suscripcion, name='suscripcion'),
    path('bloqueo/', views.bloqueo, name='bloqueo'),
    path('historial/', views.historial, name='historial'),
    path('actualizar_plan/', actualizar_plan, name='actualizar_plan'),
    path('voucher/', voucher, name='voucher'),
    path('ver_api/', views.ver_api, name='ver_api'),
    #api
    path('api/', include(routers.urls)),


]
