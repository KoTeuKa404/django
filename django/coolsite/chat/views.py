from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView

from .models import ChatMessage
from .forms import ChatMessageForm


class ChatView(LoginRequiredMixin, ListView):
    model = ChatMessage
    template_name = 'chat/chat.html'
    context_object_name = 'messages'

    def post(self, request, *args, **kwargs):
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            ChatMessage.objects.create(
                author=request.user,
                message=form.cleaned_data['message']
            )
        return redirect('chat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChatMessageForm()
        return context