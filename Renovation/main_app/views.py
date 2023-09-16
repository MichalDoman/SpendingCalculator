from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse_lazy
from django import forms
from django.core.validators import MinValueValidator

from main_app.models import Purchase, Room

SORTING_NAMES = ["item", "-item", "price", "-price", "producer", "-producer", "room", "-room", "date", "-date"]


class HomeListFilterForm(forms.Form):
    """A form used to filter purchases list"""
    key_phrase = forms.CharField(max_length=256, required=False)
    price = forms.FloatField(validators=[MinValueValidator(0)], required=False)
    room = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].choices = [(room.pk, room.name) for room in Room.objects.all()]


class HomeListView(ListView):
    """Main page purchases list view"""
    model = Purchase
    context_object_name = "items"
    form_class = HomeListFilterForm

    def get_queryset(self):
        """returns filtered and sorted queryset, according to form data and sort_by variable"""
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            key_phrase = form.cleaned_data['key_phrase']
            price = form.cleaned_data['price']
            rooms = form.cleaned_data['room']

            if key_phrase:
                queryset = queryset.filter(item__icontains=key_phrase) | queryset.filter(producer__icontains=key_phrase)

            if price:
                queryset = queryset.filter(price__gte=price)

            if rooms:
                temp_queryset = queryset.filter(room=int(rooms[0]))
                if len(rooms) > 1:
                    for room in rooms[1:]:
                        temp_queryset = temp_queryset | queryset.filter(room=int(room))
                queryset = temp_queryset

        sort_by = self.request.GET.get('sort_by', 'pk')
        if sort_by in SORTING_NAMES:
            queryset = queryset.order_by(sort_by)

        return queryset.select_related('room')

    def get_context_data(self, **kwargs):
        """adds form, total spending of currently displayed purchases and
        a sorting url with url variables of filters, that enables sorting filtered data."""

        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        queryset = self.get_queryset()

        # Get a sum of expenses:
        total = 0
        for purchase in queryset:
            total += purchase.price
        context['total'] = round(total, 2)

        # Get sorting url to keep filters:
        if self.request.method == 'GET':
            key_phrase = self.request.GET.get('key_phrase', '')
            price = self.request.GET.get('price', '')
            rooms = self.request.GET.getlist('room', [])

            filter_url = f"{self.request.path}?key_phrase={key_phrase}&price={price}"

            for room in rooms:
                url_part = f"&room={room}"
                filter_url += url_part

            context['filter_url'] = filter_url

        return context


class AddItemView(CreateView):
    """Generic view for adding purchases to the model."""
    model = Purchase
    template_name_suffix = "_add"
    fields = ["item", "producer", "price", "room", "date"]
    success_url = reverse_lazy("home")


class RegisterView(FormView):
    pass

