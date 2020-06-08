from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.forms import CharField

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):

    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field, Div
from crispy_forms.bootstrap import StrictButton
from allauth.account.forms import SignupForm   


class MyCustomSignupForm(SignupForm):

    first_name = CharField(max_length=30, label='First Name')
    last_name = CharField(max_length=30, label='Last Name')
    # email = CharField(max_length=254, label='Email')

    def save(self, request, user):
        user = super(MyCustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        return user

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)

        self.helper = helper = FormHelper()
        helper.html5_required = True

        helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            StrictButton('Отправить', css_class='btn btn-primary', type='submit'),
        )         