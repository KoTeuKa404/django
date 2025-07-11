"""
URL configuration for coolsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include,re_path
from coolsite import settings
from test_app.views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView
class MyCustomRouter(routers.SimpleRouter):
    router=[
        routers.Route(url=r'^{prefix}$',
                      mapping={'get':'list'},
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix':'List'}),
        routers.Route(url=r'^{prefix}$',
                      mapping={'get':'retrieve'},
                      name='{basename}-list',
                      detail=True,
                      initkwargs={'suffix':'Detail'}),
        ]
    
router=MyCustomRouter()

urlpatterns = [
    path('', include('test_app.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('chat/', include('chat.urls')),

    path('api/v1/librarylist/', APIList.as_view()),
    path('api/v1/librarylist/<int:pk>/', APIUpdate.as_view()),
    path('api/v1/librarydelete/<int:pk>/', APIDestr.as_view()),
    # path('api/v1/', include(router.urls)), # http://127.0.0.1:8000/api/v1/librarylist/
    
    re_path(r'^api/v1/auth/', include('djoser.urls')),  
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = PageNotFound 

