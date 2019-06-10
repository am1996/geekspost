from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
import random,string,os

def path_and_rename(instance, filename):
	rand_chars = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
	ext = filename.split('.')[-1]
	
	# set filename as random string
	random_id = "rid_%s" % (rand_chars.lower())
	filename = '{}.{}'.format(random_id, ext)
	# return the whole path to the file
	return os.path.join("media", filename)

class Posts(models.Model):
	title = models.CharField(max_length=500)
	image = models.ImageField(null=True,
							blank=True,
							width_field="width_field",
							height_field="height_field",
							upload_to=path_and_rename)
	width_field = models.IntegerField(default=0)
	height_field= models.IntegerField(default=0)
	paragraph = models.TextField(null=True,blank=True)
	slug = models.SlugField(unique=True,null=True)
	user = models.ForeignKey(User,default=1)
	date = models.DateTimeField(auto_now_add=True)

	def save(self,*args,**kwargs):
		rand_chars = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
		if kwargs.has_key('request'):
			self.user= kwargs['request'].user
		self.slug = slugify(self.title) +"-"+ rand_chars.lower()
		return super(Posts, self).save(*args,**kwargs)

	def __str__(self):
		return self.title
