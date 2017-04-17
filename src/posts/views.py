from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from posts.forms import PostForm

# Create your views here.
def post_list(request):
	queryset = Post.objects.all()
	context = {
		"object_list": queryset,
		"title": "List"
	}

	return render(request, "post_list.html", context)

def post_create(request):

	form = PostForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "Successfully Created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, "Not Created!")

	context = {
		"form": form,
	}

	return render(request, "post_form.html", context)

def post_detail(request, id=None):
	
	instance = get_object_or_404(Post,id=id)
	context = {
		"title": "Detail",
		"instance": instance,
	}

	return render(request, "post_detail.html", context)

def post_update(request, id=None):

	instance = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Updated!", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": "Detail",
		"instance": instance,
		"form": form,
	}

	return render(request, "post_form.html", context)

def post_delete(request, id=None):
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request, "Successfully Delete!")

	return redirect("posts:all")

