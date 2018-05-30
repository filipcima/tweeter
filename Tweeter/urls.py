from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Tweeter_SPJA import settings
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^addtweet$', views.addtweet, name='addtweet'),
    url(r'^discover/', views.discover, name='discover'),
    url(r'^popular/', views.popular, name='popular'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/registernewuser$', views.registernewuser, name='registernewuser'),
    url(r'^user/(?P<user_name>.+)/$', views.user),
    url(r'^tweet/(?P<id>.+)/$', views.tweet, name='tweet'),
    url(r'^tweet/(?P<id>\d+)/addcomment$', views.addcomment, name='addcomment'),
    url(r'^hashtag/(?P<hash_name>.+)/$', views.hashtag)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
