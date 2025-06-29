# urls.py
from django.urls import path
from .views import *
from django.conf.urls import handler404


urlpatterns = [
    path('', main, name='main'),
    path('shop/', shop, name='shop'),
    path('login/', LoginUser.as_view(), name='login_user'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout_user'),
    path('python/',  python.as_view(), name='python'),
    path('post/<slug:post_slug>/', show_post.as_view(), name='post'),
    path('category/<slug:cat_slug>/', show_category.as_view(), name='category'),
    path('add_page/', add_page.as_view(), name='add_page'),
    path('help/', help.as_view(), name='help'),
    path('search/', SearchView.as_view(), name='search'),
    path('tags/<slug:tag_slug>/', ShowTagPostList.as_view(), name='tag'),
    path('account/settings/', AccountSettingsView.as_view(), name='account_settings'),
    path('react/<int:post_id>/<str:reaction_type>/', react_to_post, name='react_to_post'),
    


]
