from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = "comments"
urlpatterns = [
	#comments/<pk>/delete/
	url(r'^(?P<pk>[0-9]+)/delete$',
	views.DeleteComment.as_view(),name="comment_delete"),
	#comments/<pk>/edit/
	url(r'^(?P<pk>[0-9]+)/edit$',
	views.EditComment.as_view(),name="comment_edit"),
]