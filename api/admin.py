from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin

# from .forms import UserBotsChangeListForm
# from .models import UserBots
from .forms import CustomUserCreationForm, CustomUserChangeForm, TokenForm
from .models import CustomUser, Token, Task, Keyboard, Message
from .models import Bot


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bots',)}),
    )


class TokenAdmin(ModelAdmin):
    add_form = TokenForm
    form = TokenForm
    model = Token
    list_display = ["name", "service", "is_supertoken"]


class KeyboardAdmin(ModelAdmin):
    list_display = ["name", "bot"]

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Use special form during foo creation
    #     """
    #     defaults = {}
    #     if obj is None:
    #         defaults['form'] = self.add_form
    #     defaults.update(kwargs)
    #     return super().get_form(request, obj, **defaults)


class MessageAdmin(ModelAdmin):
    list_display = ["name", "bot"]


# Register your models here.

admin.site.register(Bot)
admin.site.register(Token, TokenAdmin)
admin.site.register(Task)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Keyboard, KeyboardAdmin)
admin.site.register(Message, MessageAdmin)
