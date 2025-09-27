# urls.py
from django.urls import path
from .views import *
from django.conf.urls import handler404
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', main, name='main'),
    path('shop/', shop, name='shop'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutUser, name='logout_user'),
    path('python/',  Python.as_view(), name='python'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/delete/', DeletePost.as_view(), name='delete_post'),
    path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='category'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('help/', Help.as_view(), name='help'),
    path('search/', SearchView.as_view(), name='search'),
    path('tags/<slug:tag_slug>/', ShowTagPostList.as_view(), name='tag'),
    path('account/settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('react/<int:post_id>/<str:reaction_type>/', react_to_post, name='react_to_post'),
    path("test/",test,name='test')


]
