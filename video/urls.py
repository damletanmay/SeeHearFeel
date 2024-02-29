from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name = "home"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('add_file/',views.add_file,name="add_file"),
    path('animation/',views.animation_view,name='animation'),
    path('about/',views.about_view,name='about'),
    path('drive/',views.drive,name='drive'),
    path('contact/',views.contact_view,name='contact'),
    path('<int:video_id>/video/',views.show_video,name='show_video'),
]
