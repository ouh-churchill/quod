from django.conf.urls import url
from .views import index
from .views import ViewAll
from .views import ViewAllPublic
from .views import ViewAllForm


urlpatterns = [
    url(r'^$', index, name='index'),
	url(r'all', ViewAll.as_view()),
    url(r'public', ViewAllPublic.as_view()),
    url(r'form', ViewAllForm.as_view()),
]