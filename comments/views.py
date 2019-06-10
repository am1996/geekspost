from .models import Comments
from posts.models import Posts
from django.views import generic
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,Http404
from django.urls import reverse,reverse_lazy

# Create your views here.
class DeleteComment(generic.edit.DeleteView):
	model=Comments
	def get_success_url(self):
		post_id = self.get_object().object_id
		post_slug = Posts.objects.get(pk = post_id).slug
		return reverse("posts:post_detail",kwargs={"slug":post_slug})
	def dispatch(self,request,*args,**kwargs):
			comment = Comments.manager.get(pk = kwargs['pk'])
			if comment.user != request.user:
				raise Http404("Page not found")
			return super(DeleteComment, self).dispatch(request,*args, **kwargs)

class EditComment(generic.edit.UpdateView):
	model = Comments
	template_name="form.html"
	fields = ["paragraph"]
	def get_success_url(self):
		post_id = self.get_object().object_id
		post_slug = Posts.objects.get(pk = post_id).slug
		return reverse("posts:post_detail",kwargs={"slug":post_slug})
	def dispatch(self,request,*args,**kwargs):
		comment = self.get_object()
		if comment.user != request.user:
			raise Http404("Page not found")
		return super(EditComment, self).dispatch(request,*args, **kwargs)