from django.conf.urls import include, url

from rest_framework import routers

from teams import views


app_name = 'teams'


router = routers.DefaultRouter()
router.register(r'teams', views.TeamListViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^members/(?P<pk>[0-9]+)/$', views.TeamMemberDetailView.as_view(), name='member-detail'),      # noqa
    url(r'^teams/(?P<pk>[0-9]+)/invites/$', views.TeamInviteListView.as_view(), name='team-invites'),   # noqa
]
