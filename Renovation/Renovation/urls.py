from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

from main_app.views import HomeListView, AddItemView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', HomeListView.as_view(), name='home'),
    path('add-item/', AddItemView.as_view(), name="add_item"),
]
