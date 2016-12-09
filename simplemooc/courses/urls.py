from django.conf.urls import url
from simplemooc.courses.views import list, details, enrollment, announcements


urlpatterns = [
    url(r'^$', list, name='index'),
    # url(r'^(?P<pk>\d+)/$', details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/$', details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', enrollment, name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/$', announcements, name='announcements'),
]
