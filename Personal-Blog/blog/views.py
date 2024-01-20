from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from datetime import date
from django.urls import reverse
from django.views import View

from .models import Post
from .forms import CommentForm

# Create your views here.

def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(request,"blog/index.html",{"posts": latest_posts})

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request,"blog/all-posts.html",{"all_posts":all_posts})

def posts_detail(request, slug):
    identified_post = Post.objects.get(slug=slug)
    post_tags = identified_post.tags.all()
    
    # To check whether the post we are dealing with is a read later post or not..
    stored_posts = request.session.get("stored_posts")
    if stored_posts is not None:
        is_saved_for_later = identified_post.id in stored_posts
    else:
        is_saved_for_later = False 
   
    all_comments = identified_post.comments.all().order_by("-id")
    if request.method=="GET":
        return render(request,"blog/post-detail.html",{
            "post":identified_post,
            "post_tags":post_tags,
            "comment_form":CommentForm(),
            "comments":all_comments,
            "is_saved_for_later":is_saved_for_later})
    elif request.method=="POST":
        comment_form = CommentForm(request.POST)
        # To display the latest comment first
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = identified_post
            comment.save()
            return HttpResponseRedirect(reverse("posts-detail-page",args=[slug]))
        
        return render(request,"blog/post-detail.html",{
            "post":identified_post,
            "post_tags":post_tags,
            "comment_form":comment_form,
            "comments":all_comments,
            "is_saved_for_later":is_saved_for_later})


class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            #Get the posts objects for which id's are in stored_posts list
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request,"blog/stored-posts.html",context)


    def post(self,request):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")
