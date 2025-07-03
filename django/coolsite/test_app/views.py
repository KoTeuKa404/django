import os
import aiofiles

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render

from rest_framework.response import *
from rest_framework.views import *
from rest_framework import generics, viewsets 
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination

from asgiref.sync import sync_to_async

from .forms import *
from .models import *
from .utils import *
from .API.serializers import librarySerializer
from .permission import *

###############################################################################>
# venv\Scripts\activate
###############################################################################>
# docker compose up
# docker compose restart web
# docker compose down
# docker compose up -d --build


class Python(DataMixin, ListView):
    model = library
    template_name = 'test_app/python.html'
    context_object_name = 'posts'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Python бібліотеки')
        return {**context, **c_def}

    def get_queryset(self):
        return library.objects.filter().select_related('cat')


class add_page(LoginRequiredMixin,DataMixin,CreateView):
    form_class = AddPostForm
    template_name = 'test_app/addpage.html'
    success_url = reverse_lazy('python')
    login_url = '/admin/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user  
        post.save()
        return redirect(self.success_url)
    def get_context_data(self, *, objects_list = None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Добавлення статті")
        return dict(list(context.items())+list(c_def.items()))
    

class ShowPost(DataMixin, FormMixin, DetailView):
    model = library
    template_name = 'test_app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(unapproved=False)
        context['form'] = self.get_form()

        # НЕ ВИКЛИКАТИ НІЧОГО ЛИШНЬОГО ПО ТИПУ YouTubeVideoInfo чи будь які інші зовнішні бібліотеки .
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.author = self.request.user
        comment.save()
        return redirect('post', post_slug=self.object.slug)



class ShowCategory(DataMixin, ListView):
    model = library
    template_name = 'test_app/python.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return library.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)     
        if context.get('posts'):
            title = 'Категорія - ' + str(context['posts'][0].cat)
            cat_selected = context['posts'][0].cat_id
        else:
            title = 'Категорія без записів'
            cat_selected = None         
        c_def = self.get_user_context(title=title, cat_selected=cat_selected)   
        return dict(list(context.items()) + list(c_def.items()))


class ShowTagPostList(DataMixin, ListView):
    model = library
    template_name = 'test_app/python.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs.get('tag_slug'))
        context.update(self.get_user_context(title=f"Теги: {tag.tag}"))
        context.update({'tags': TagPost.objects.all(), 'tag': tag})
        return context

    def get_queryset(self):
        tag = get_object_or_404(TagPost, slug=self.kwargs.get('tag_slug'))
        return library.objects.filter(tags=tag)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'test_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('python')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'test_app/login.html'
    success_url = reverse_lazy('python')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вхід")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('python')


class Help(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'test_app/help.html'
    success_url = reverse_lazy('python')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Зворотній звязок")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        data = form.cleaned_data
        report_content = f"Name: {data['name']}\nEmail: {data['email']}\nContent: {data['content']}\n"

        report_dir = os.path.join('media', 'report')
        os.makedirs(report_dir, exist_ok=True)
        report_file_path = os.path.join(report_dir, f"report_{data['name']}_{data['email']}.txt")

        with open(report_file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(report_content)

        return redirect('python')


class SearchView(DataMixin, ListView):
    model = library
    template_name = 'test_app/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            if query.startswith('#'):
                tag_query = query[1:]
                tags = TagPost.objects.filter(tag__icontains=tag_query)
                categories = Category.objects.filter(name__icontains=tag_query)
                return library.objects.filter(tags__in=tags) | library.objects.filter(cat__in=categories)
            return library.objects.filter(title__icontains=query).select_related('cat')
        return library.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Результати пошуку:')
        context['query'] = self.request.GET.get('q')
        return dict(list(context.items()) + list(c_def.items()))


def LogoutUser(request):
    logout(request)
    return redirect('python')


class AccountSettingsView(LoginRequiredMixin, TemplateView,DataMixin):
    template_name = 'test_app/account_settings.html'
    success_url = reverse_lazy('account_settings')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        context['password_form'] = CustomPasswordChangeForm(user=self.request.user)
        c_def = self.get_user_context(title='User Profile')
        context.update(c_def)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(self.request.user, request.POST) 

        if 'update_profile' in request.POST:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('account_settings')

        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('account_settings')

        context = self.get_context_data()
        context['user_form'] = user_form
        context['password_form'] = password_form
        return self.render_to_response(context)

@login_required
async def react_to_post(request, post_id, reaction_type):
    post = await library.objects.aget(id=post_id)
    user_reaction, created = await Reaction.objects.aget_or_create(user=request.user, post=post)

    if not created:
        if user_reaction.reaction == reaction_type:
            await sync_to_async(user_reaction.delete)()
            if reaction_type == 'L':
                if post.likes > 0:
                    post.likes -= 1
            else:
                if post.dislikes > 0:
                    post.dislikes -= 1
        else:
            if user_reaction.reaction == 'L':
                if post.likes > 0:
                    post.likes -= 1
                post.dislikes += 1
            else:
                post.likes += 1
                if post.dislikes > 0:
                    post.dislikes -= 1
            user_reaction.reaction = reaction_type
            await sync_to_async(user_reaction.save)()
    else:
        if reaction_type == 'L':
            post.likes += 1
        else:
            post.dislikes += 1
        user_reaction.reaction = reaction_type
        await sync_to_async(user_reaction.save)()

    await sync_to_async(post.save)()
    return redirect('post', post_slug=post.slug)



def pageNotFound(request, exception):
    return render(request, 'test_app/404.html', status=404)


class VideoInfoError(Exception):
    """Custom exception for video info errors."""
    pass


#######################################################################


#######################################################################

     #       ###       #
    # #      #  #      
   #####     ###       #
  #     #    #         #
 #       #   #         #
    
#######################################################################

        
        
class Pagination(PageNumberPagination):
    page_size=3
    page_size_query_param='page_size'
    max_page_size=100
    
class APIList(generics.ListCreateAPIView):
    queryset = library.objects.all()
    serializer_class = librarySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JWTAuthentication,)
    pagination_class=Pagination
    
class APIUpdate(generics.RetrieveUpdateAPIView):
    queryset=library.objects.all()
    serializer_class=librarySerializer
    permission_classes=(IsAdminOrOwnerOrReadOnly,) 
    # permission_classes=(IsAuthenticated,) 
    authentication_classes=(TokenAuthentication,)
    
class APIDestr(generics.RetrieveUpdateDestroyAPIView):
    queryset=library.objects.all()
    serializer_class=librarySerializer
    permission_classes=(IsAdminOrOwnerOrReadOnly,)








    # # queryset=library.objects.all()
    # serializer_class=librarySerializer    

    # def get_queryset(self):
    #     pk=self.kwargs.get('pk')    
    #     if not pk:
    #         return library.objects.all()
    #     return library.objects.filte(pk=pk)

    # @action(methods=['get'], detail=True)
    # def category(self,request,pk=None):  
    #     cats=Category.objects.get(pk=pk)
    #     return Response({'cats':cats.name})

# class APIPython(generics.ListAPIView, APIView):
#     def get(self, request):
#         l = library.objects.all()
#         return Response({'posts': librarySerializer(l, many=True).data})

#     def post(self, request):
#         serializer = librarySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response({'post': serializer.data})

#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         if not pk:
#             return Response({'error': "PK is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             instance = library.objects.get(pk=pk)
#         except library.DoesNotExist:
#             return Response({"error": "Library object not found"}, status=status.HTTP_404_NOT_FOUND)

#         serializer = librarySerializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})








































def test(request):
    posts=library.objects.all()
    return render(request,'test_app/test.html',{'posts':posts,'title':'test'})



#Main
async def main(request):
    posts = await sync_to_async(list)(library.objects.all())
    categories = await sync_to_async(list)(Category.objects.all())

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'головна сторінка',
        'cat_selected': 0,
        'title':'Головна сторінка',        
        'categories': categories,
    }
    return render(request, 'test_app/main.html', context=context)




def shop(request):
    return render(request, 'test_app/shop.html')



