from django.contrib import admin
from django.urls import path

from main_app.views import HomeListView, AddItemView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeListView.as_view(), name='home'),
    path('add-item/', AddItemView.as_view(), name="add_item"),
]
