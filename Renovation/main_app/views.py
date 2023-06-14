from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django import forms
from django.core.validators import MinValueValidator

from main_app.models import Purchase, Room


class HomeListFilterForm(forms.Form):
    key_phrase = forms.CharField(max_length=256, required=False)
    price = forms.FloatField(validators=[MinValueValidator(0)], required=False)
    room = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].choices = [(room.pk, room.name) for room in Room.objects.all()]


class HomeListView(ListView):
    model = Purchase
    context_object_name = "items"
    form_class = HomeListFilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('room')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class AddItemView(CreateView):
    model = Purchase
    template_name_suffix = "_add"
    fields = ["item", "producer", "price", "room", "date"]
    success_url = reverse_lazy("home")
