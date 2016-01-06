from django.conf.urls import patterns, url
from webapp import views


urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^(?P<uri>[0-9a-z]{6,})$', views.Home.as_view(), name="code_url"),
    url(r'^api/run/$', views.source_compile_and_run),
    url(r'^history/(?P<uri>[0-9a-z]{6,})$', views.code_history),
]
