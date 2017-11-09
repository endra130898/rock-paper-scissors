from django.conf.urls import url
from .views import index, submit_flag_without_admin

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^create_flag$', submit_flag_without_admin, name='create-flag'),
]