from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, FilteredSelectMultiple
from django.contrib.admin import site
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import Bot, Token

# class UserBotsChangeListForm(forms.ModelForm):
#     bots = forms.ModelMultipleChoiceField(queryset=Bot.objects.all(), required=False)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    bots = forms.ModelMultipleChoiceField(queryset=None, label='Select bots', required=False)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['bots'].widget = RelatedFieldWidgetWrapper(FilteredSelectMultiple('bots', False, ),
                                                               CustomUser._meta.get_field('bots').remote_field,
                                                               admin_site=site)
        self.fields['bots'].queryset = Bot.objects.all()

    class Media:
        ## media for the FilteredSelectMultiple widget
        css = {
            'all': ('/media/css/widgets.css',),
        }
        # jsi18n is required by the widget
        js = ('/admin/jsi18n/',)

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class TokenForm(ModelForm):
    bots = forms.ModelMultipleChoiceField(queryset=None, label='Select bots', required=False)

    def __init__(self, *args, **kwargs):
        super(TokenForm, self).__init__(*args, **kwargs)
        self.fields['bots'].widget = RelatedFieldWidgetWrapper(FilteredSelectMultiple('bots', False, ),
                                                               Token._meta.get_field('bots').remote_field,
                                                               admin_site=site)
        self.fields['bots'].queryset = Bot.objects.all()

    class Media:
        ## media for the FilteredSelectMultiple widget
        css = {
            'all': ('/media/css/widgets.css',),
        }
        # jsi18n is required by the widget
        js = ('/admin/jsi18n/',)

    class Meta:
        model = Token
        fields = ("name", "service", "bots", "is_supertoken")
