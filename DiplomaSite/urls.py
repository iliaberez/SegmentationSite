from django.urls import path, include
from DiplomaSite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('login/', views.LoginUser.as_view(), name='login'), 
    path('logout/', views.logout_user, name='logout'),  
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('segmentation/', views.segmentation, name='segmentation'),
    path('history/', views.history, name='history'),
    path('segmentations/<int:SegPostId>/', views.details)
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
