from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from posts.models import Posts

# Create your models here.
class CommentsManager(models.Manager):
	def instance_filter(self,instance):
		#getting content type for passed instance of the class
		content_type = ContentType.objects.get_for_model(instance.__class__)
		#getting primary key of that instance
		obj_id = instance.pk
		"""
		filtering to get comments that has the same content
		and object id
		"""
		qs = super(CommentsManager,self).filter(
			content_type = content_type,
			object_id = obj_id)
		return qs

class Comments(models.Model):
	manager 	   = CommentsManager()
	user 	  	   = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
	paragraph      = models.TextField()
	content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id	   = models.PositiveIntegerField()
	#content object is the object containing the comment
	content_object = GenericForeignKey('content_type', 'object_id')
	def __str__(self):
		return self.paragraph