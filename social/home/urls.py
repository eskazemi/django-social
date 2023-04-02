from .views import (
    HomeView,
    PostDetailView,
    PostDeleteView,
    PostUpdateView
)
from django.urls import path


app_name = "home"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('post/detail/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name="detail"),
    path('post/delete/<int:post_id>/', PostDeleteView.as_view(), name="delete"),
    path('post/update/<int:post_id>/', PostUpdateView.as_view(), name="update"),
]
