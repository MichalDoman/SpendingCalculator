from django.views.generic import ListView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User

from main_app.forms import HomeListFilterForm, RegisterForm
from main_app.models import Purchase

SORTING_NAMES = ["item", "-item", "price", "-price", "producer", "-producer", "room", "-room", "date", "-date"]


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
    """A View that enables users to register via a form, and access all functionalities."""
    form_class = RegisterForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        password_repeated = form.cleaned_data['password_repeated']

        if User.objects.filter(email=email).exists():
            form.add_error(None, 'This e-mail address is already taken!')
            return super().form_invalid(form)

        if password != password_repeated:
            form.add_error(None, 'Passwords did not match!')
            return super().form_invalid(form)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )

        login(self.request, user)
        return super().form_valid(form)
