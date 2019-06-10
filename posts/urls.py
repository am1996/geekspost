from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = "posts"
urlpatterns = [
    #posts/
    url(r'^$', views.PostList.as_view() ,name="index"),
    #/posts/post/<slug>
    url(r'^(?P<slug>[0-9a-zA-Z -]+)$',
    views.PostDetails.as_view() ,name="post_detail"),
    #Post/create
    url(r'^create/$', views.CreatePost.as_view(),name="post_create"),
    #post/delete/<slug>
    url(r"^delete/(?P<slug>[0-9a-zA-Z -]+)$",
    views.DeletePost.as_view(),name="post_delete"),
    #post/edit/<slug>
    url(r"^edit/(?P<slug>[0-9a-zA-Z -]+)$",
    views.EditPost.as_view(),name="post_edit"),

    #posts/register
    url(r"^register/",views.Register.as_view() ,name="register"),
    #posts/login
    url(r"^login/",views.Login.as_view() ,name="login"),
    #posts/logout
    url(r"^logout/",views.LogoutView.as_view() ,name="logout"),
    #msuic/<user>/dashboard
    url(r"^users/(?P<username>[0-9a-zA-Z -]+)/$", 
    views.DashBoardView.as_view(),name="dashboard"),
    #posts/<username>/edit
    url(r"^users/(?P<username>[0-9a-zA-Z -]+)/edit", 
    views.EditUser.as_view(),name="edit_user"),

    #posts/<slug>/create_comment
    url(r'^(?P<slug>[0-9a-zA-Z -]+)/add_comment',
    views.CreateComment.as_view(),name="CreateComment"),

]