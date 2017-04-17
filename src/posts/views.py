from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from posts.models import Post
from posts.forms import PostForm

# Create your views here.
def post_list(request):
	queryset = Post.objects.all()
	context = {
		"object_list": queryset,
		"title": "List"
	}

	return render(request, "index.html", context)

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
		messages.success(request, "Successfully Updated!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": "Detail",
		"instance": instance,
		"form": form,
	}

	# return HttpResponse("<h1>List</h1>")
	return render(request, "post_form.html", context)

def post_delete(request):

	return HttpResponse("<h1>Delete</h1>")
