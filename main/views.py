from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from api.models import Bot  # , UserBots

# Create your views here.
from django.views import generic

from django.conf import settings


def is_ingroup(user: settings.AUTH_USER_MODEL, group_name: str):
    return user.groups.filter(name=group_name).exists()


class BotListView(generic.ListView):
    model = Bot
    context_object_name = 'bot_list'
    queryset = Bot.objects.all()
    template_name = 'main/index.html'

    def get_queryset(self):
        queryset = super(BotListView, self).get_queryset()
        user: settings.AUTH_USER_MODEL = self.request.user
        if user.is_superuser or is_ingroup(user, "Admin"):
            return queryset
        try:
            # userbot: UserBots = UserBots.objects.get(user=user)
            # return userbot.bots.all()
            return user.bots.all()
        except:
            return Bot.objects.none()
