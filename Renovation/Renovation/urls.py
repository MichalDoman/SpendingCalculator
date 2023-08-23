from django.contrib import admin
from django.urls import path, include

from main_app.views import HomeListView, AddItemView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('', HomeListView.as_view(), name='home'),
    path('add-item/', AddItemView.as_view(), name="add_item"),
]
