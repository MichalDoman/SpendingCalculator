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
        form = self.form_class(self.request.GET)
        if form.is_valid():
            key_phrase = form.cleaned_data['key_phrase']
            price = form.cleaned_data['price']
            rooms = form.cleaned_data['room']

            if key_phrase:
                queryset = queryset.filter(item__icontains=key_phrase) | queryset.filter(producer__icontains=key_phrase)

            if price:
                queryset = queryset | queryset.filter(price__gte=price)

            if rooms:
                temp_queryset = queryset.filter(room=int(rooms[0]))
                if len(rooms) > 1:
                    for room in rooms[1:]:
                        temp_queryset = temp_queryset | queryset.filter(room=int(room))
                queryset = temp_queryset

        return queryset.select_related('room')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        queryset = self.get_queryset()

        total = 0
        for purchase in queryset:
            total += purchase.price
        context['total'] = round(total, 2)

        return context


class AddItemView(CreateView):
    model = Purchase
    template_name_suffix = "_add"
    fields = ["item", "producer", "price", "room", "date"]
    success_url = reverse_lazy("home")
