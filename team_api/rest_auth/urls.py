from django.conf.urls import url

from rest_auth import views


urlpatterns = [
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^register/$', views.RegistrationView.as_view()),
]
