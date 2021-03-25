import json
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import ChatRoom
from .forms import ChatRoomCreateForm
from .mixins import OwnerOnlyMixin

User = get_user_model()


class RoomListView(LoginRequiredMixin, View):
    template_name = 'chat/index.html'

    def get(self, request):
        user = request.user
        room_list = user.user_rooms.all()
        return render(request, self.template_name, {'room_list': room_list})


class ChatRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super(ChatRoomView, self).get_context_data(**kwargs)
        context["user"] = mark_safe(json.dumps(self.request.user.name))
        context["room_name"] = mark_safe(json.dumps(kwargs['room_name']))
        context["room_list"] = self.request.user.user_rooms.all()
        context['room_obj'] = ChatRoom.objects.get(name=kwargs['room_name'])
        return context


class SearchResultsView(LoginRequiredMixin, View):
    template_name = 'chat/search_results.html'

    def get(self, *args, **kwargs):
        query = self.request.GET.get('q')
        room_list = ChatRoom.objects.filter(
            name__icontains=query)
        user_list = User.objects.filter(
            name__icontains=query).exclude(pk=self.request.user.pk)
        return render(self.request, self.template_name, {
            'room_list': room_list,
            'user_list': user_list
        })


class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    form_class = ChatRoomCreateForm
    template_name = 'chat/create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.object.members.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('chat:room', kwargs={
            "room_name": self.object.name})


class PrivateRoomCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        second_user = User.objects.filter(name=kwargs['second_user'])[0]
        private_room, created = ChatRoom.objects.get_or_create(
            is_private=True,
            name=f"{request.user.name}_{second_user.name}",
            owner=request.user,
            second_user=second_user,
        )
        if private_room:
            private_room.members.add(second_user, request.user)
        return HttpResponseRedirect(reverse_lazy(
            'chat:room', kwargs={'room_name': private_room.name}))


class ChatRoomUpdateView(LoginRequiredMixin, OwnerOnlyMixin, UpdateView):
    template_name = 'chat/update.html'
    model = ChatRoom
    form_class = ChatRoomCreateForm

    def get_success_url(self):
        return reverse_lazy('chat:room',
                            kwargs={"room_name": self.object.name})


class ChatRoomDeleteView(LoginRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = ChatRoom
    success_url = reverse_lazy('chat:index')
