from .models import *
from django.db.models import Count
from django.core.cache import cache
from django.core.paginator import Paginator

menu = [
    {'title': "Про сайт", 'url_name': 'python'},
    {'title': "Головний сайт ", 'url_name': 'main'},
    {'title': "Добавити статью", 'url_name': 'add_page'},
    {'title': "Зворотній зв'язок", "url_name": 'help'},
    {'title': "Чат", "url_name": 'chat'}

]


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('library'))
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            for index in sorted([2, 3], reverse=True):
                user_menu.pop(index)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = None
        # if 'cat_selected' == 0:
        #     context['cat_selected'] = 0
        return context
