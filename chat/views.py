from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from chat.forms import CreateMessage, UserRegistrationForm, UserLoginForm
from chat.models import Message, CustomUser


def get_first_message_id(user: CustomUser) -> int:
    first_message_id = user.last_message_id
    if first_message_id == 0:
        last_message = Message.objects.last()
        if not last_message:
            first_message_id = 1
        else:
            last_message_id = last_message.id
            if last_message_id >= 10:
                first_message_id = last_message_id - 9
            else:
                first_message_id = 1
        user.last_message_id = first_message_id
        user.save()
    return first_message_id


class PrintChatView(LoginRequiredMixin, CreateView):
    template_name = 'chat/chat.html'
    form_class = CreateMessage
    success_url = reverse_lazy('chat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        first_message_id = get_first_message_id(self.request.user)
        context['messages'] = Message.objects.filter(id__gte=first_message_id)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        return super().get(self.request, *args, **kwargs)


class LoginUserView(LoginView):
    form_class = UserLoginForm
    template_name = 'chat/login.html'


class RegisterUserView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'chat/register.html'
    success_url = reverse_lazy('login')


@login_required
def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('chat'))
