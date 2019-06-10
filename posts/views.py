from django.contrib.auth import authenticate,login
from .models import Posts
from comments.models import Comments
from django.contrib.contenttypes.models import ContentType
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect,Http404
from django.urls import reverse,reverse_lazy
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout
import os
# Create your views here.


"""
(1) edit post doesn't delete image on changing it -> django-cleanup
"""

#posts
class PostList(generic.ListView):
	context_object_name="posts"
	template_name="list.html"
	def get_queryset(self):
		try:
			q = self.request.GET["q"]
		except Exception as error:
			q = None
		if q:
			query = (
					Q(title__icontains= q)|
					Q(paragraph__icontains= q)
					)
			posts = Posts.objects.filter(query)
		else:
			posts = Posts.objects.all()
		paginator = Paginator(posts, 3)
		page = self.request.GET.get('page')
		try:
			qs = paginator.page(page)
			return qs
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			qs = paginator.page(1)
			return qs
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			qs = paginator.page(paginator.num_pages)
			return qs

class CreatePost(generic.edit.CreateView):
	model = Posts
	template_name="form.html"
	fields = ['title',"paragraph","image"]
	def dispatch(self,request,*args,**kwargs):
		post = self.model()
		if(request.user.is_authenticated):
			post.user = request.user
			return super(CreatePost, self).dispatch(request,*args,**kwargs)
		else:
			raise Http404("Page not found")
	def post(self,request,*args,**kwargs):
		post = self.model()
		if(request.user.is_authenticated):
			post.user     = request.user
			post.title    = request.POST['title']
			post.paragraph= request.POST['paragraph']
			try:
				post.image    = request.FILES['image']
			except:
				pass
			post.save()
			return HttpResponseRedirect(
				reverse("posts:index",)
				)

class DeletePost(generic.edit.DeleteView):
	model=Posts
	template_name = "post_delete_confirm.html"
	success_url = reverse_lazy("posts:index")
	def dispatch(self,request,*args,**kwargs):
		post = Posts.objects.get(slug = kwargs.get("slug"))
		if post.user != request.user:
			raise Http404("Page not found")
		if(post.image != "" and os.path.isfile("."+post.image.url)):
			os.remove("."+post.image.url)
		return super(DeletePost, self).dispatch(request,*args, **kwargs)

class EditPost(generic.edit.UpdateView):
	model = Posts
	template_name="form.html"
	fields = ['title',"paragraph",'image']
	def dispatch(self,request,*args,**kwargs):
		post = self.get_object()
		if post.user != request.user:
			raise Http404("Page not found")
		return super(EditPost, self).dispatch(request,*args, **kwargs)
	def get_success_url(self):
		return reverse("posts:index")

class PostDetails(generic.DetailView):
	model=Posts
	context_object_name = "post"
	template_name="detail.html"
	def get_context_data(self, **kwargs):
		context = super(PostDetails, self).get_context_data(**kwargs)
		context['comments']=Comments.manager.instance_filter(self.get_object())
		return context
#posts end


#comments
class CreateComment(generic.edit.CreateView):
	model = Comments
	template_name="detail.html"
	fields = ["paragraph"]
	def dispatch(self,request,*args,**kwargs):
		if(request.user.is_authenticated):
			return super(CreateComment, self).dispatch(request,*args,**kwargs)
		else:
			raise Http404("Page not found")
	def post(self,request, *args, **kwargs):
		comment = self.model() #get current created comment
		#comment.post = Posts.objects.get(slug=kwargs['slug'])
		comment.object_id = Posts.objects.get(slug=kwargs['slug']).pk
		comment.content_type = ContentType.objects.get_for_model(Posts)
		comment.paragraph = request.POST['paragraph']
		comment.user = request.user
		comment.save()
		return HttpResponseRedirect(
			reverse("posts:post_detail",kwargs={"slug":kwargs['slug']})
			)
#comments end


#users
class Register(generic.View):
	template_name="form.html"
	form_class = RegisterForm
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			raise Http404("page not found")
		else:
			return render(request, self.template_name,{
			"form":self.form_class
			})
	def post(self,request,*args,**kwargs):
		user = self.form_class(request.POST)
		try:
			user = user.save(commit=False)
			#sets the password with hash algorithm
			user.set_password(user.password)
			user.is_active = True
			user.save()
			return redirect("/")
		except:
			return render(request, self.template_name,{
				"error":"This user already exists.",
				"form":self.form_class
				})

class Login(generic.View):
	template_name="form.html"
	form_class = LoginForm
	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			raise Http404("Page not found")
		else:
			return render(request, self.template_name,{
				"form":self.form_class
				})
	def post(self,request,*args,**kwargs):
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username=username,password=password)
		if user is not None:
			login(request, user)
			return redirect("posts:index")

		else:
			return render(request, self.template_name,{
				"error":"username and password doesn't match",
				"form":self.form_class
				})

class LogoutView(generic.RedirectView):
	def get(self,request):
		logout(request)
		return redirect("posts:index")

class EditUser(generic.UpdateView):
	model=User
	slug_url_kwarg = "username"
	slug_field = 'username'
	fields=["username","email","first_name","last_name"]
	template_name="form.html"
	def dispatch(self,request,*args,**kwargs):
		user = self.get_object()
		if user != request.user:
			raise Http404("Page not found")
		return super(EditUser, self).dispatch(request,*args, **kwargs)

	def get_success_url(self):
		return reverse("posts:index")

class DashBoardView(generic.View):
	model = Posts
	template_name = "dashboard.html"
	def dispatch(self,request,*args,**kwargs):
		if not request.user.is_authenticated:
			raise Http404("page not found")
		return render(request,self.template_name,{
				"posts":self.model,
			})
#users end