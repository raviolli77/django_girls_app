from django.shortcuts import render
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

# Create your views here.
def post_list(request):
    """
	Creates a 'view' of our post lists where its ordered by most recent
	publised date using QuerySets

    """
    posts = Post.objects.filter(published_date__lte=timezone.now())\
    .order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if not request.user.is_staff:
        raise Http404
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Removing this allows to save as drafts
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    if not request.user.is_staff:
        raise Http404    
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Removing this allows to save as drafts
            #post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    if not request.user.is_staff:
        raise Http404    
    posts = Post.objects.filter(published_date__isnull=True)\
    .order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    if not request.user.is_staff:
        raise Http404    
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    if not request.user.is_staff:
        raise Http404    
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
    
def index(request):
   return render(request, "blog/index.html", {})