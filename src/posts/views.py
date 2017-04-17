from urllib import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from posts.models import Post
from posts.forms import PostForm

# Create your views here.
def post_list(request):
	
	queryset_list = Post.objects.all().order_by("-timestamp")
	paginator = Paginator(queryset_list,25)

	page_request_var = "page"
	page = request.GET.get(page_request_var)

	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset,
		"title": "List",
		"page_request_var": page_request_var
	}

	return render(request, "post_list.html", context)

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	# if not request.user.is_authenticated():
	# 	raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
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
	share_string = quote_plus(instance.content)

	context = {
		"title": "Detail",
		"instance": instance,
	}

	return render(request, "post_detail.html", context)

def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
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
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request, "Successfully Delete!")

	return redirect("posts:all")

