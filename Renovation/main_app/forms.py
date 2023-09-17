from django import forms
from django.core.validators import MinValueValidator

from main_app.models import Room


class HomeListFilterForm(forms.Form):
    """A form used to filter purchases list"""
    key_phrase = forms.CharField(max_length=256, required=False)
    price = forms.FloatField(validators=[MinValueValidator(0)], required=False)
    room = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].choices = [(room.pk, room.name) for room in Room.objects.all()]


class RegisterForm(forms.Form):
    """A form used for registering new users."""
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    repeated_password = forms.CharField(widget=forms.PasswordInput)
