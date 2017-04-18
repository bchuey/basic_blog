from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save

from django.utils import timezone
from django.utils.text import slugify


# Create your models here.

## model manager
class PostManager(models.Manager):

	# Post.objects.all()
	# overriding .all() function
	# def all(self, *args, **kwargs):
	# 	return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

	def active(self, *args, **kwargs):
		return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)


class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, 
		null=True, 
		blank=True, 
		width_field="width_field", 
		height_field="height_field"
	)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

	# sync model manager
	# 'objects' is convention -- can name whatever
	objects = PostManager()

	# python2
	def __unicode__(self):
		return self.title

	# python3
	def __str__(self):
		return self.title

	def get_absolute_url(self):

		return reverse("posts:detail", kwargs={"id":self.id})
		# return "/posts/%s/" %(self.id)

	# class Meta:
		# order = ["-timestamp"]

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

# runs before .save() is called
def pre_save_post_signal_receiver(sender, instance, *args, **kwargs):

	# slug = slugify(instance.title)
	# exists = Post.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug = "%s-%s" %(slug, instance.id)

	# instance.slug = slug
	if not instance.slug:
		instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_signal_receiver, sender=Post)