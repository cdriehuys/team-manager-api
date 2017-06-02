from django.conf.urls import include, url

from rest_framework import routers

from teams import views


app_name = 'teams'


router = routers.DefaultRouter()
router.register(r'teams', views.TeamListViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
