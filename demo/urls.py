from django.urls import path, include
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('qr/', views.qr, name='qr'),
    path('qr_code/', views.Qrcode, name='qrcode'),
       path('insta/', views.insta, name='insta'),
     path('insta_download/', views.insta_download, name='insta_download'),
    path('sample/', views.sample, name='sample'),
    path('user/<str:name>/',views.user,name="user"),
    
    path('pdf_protect/',views.pdf_protect, name='pdf_protect'),
    path('pdf_process/',views.pdf_process, name='pdf_process'),
    path('text/',views.text, name='text'),
     path('text_process/',views.text_process, name='text_process'),
    path('stego/',views.stego, name='stego'),
    path('encode/',views.encode, name='encode'),
    path('return_encoded/',views.return_encoded, name='return_encoded'),
    path('decoded/',views.decoded, name='decoded'),
    path('get_signup/',views.get_signup, name='get_signup'),
    path('signup/',views.signup, name='signup'),
 path('get_login/',views.get_login, name='get_login'),   
    path("login/",views.login_view,name="login"),
    path("get_logout/",views.get_logout,name="get_logout"),
]
