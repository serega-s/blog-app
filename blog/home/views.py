import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import BlogForm, NewCommentForm
from .models import BlogModel, Comment, Profile


def home(request):
    context = {
        'posts': BlogModel.objects.order_by('-updated_at').filter(is_draft=False),
        'featured_post': BlogModel.objects.filter(featured=True).last()
    }
    return render(request, 'home/home.html', context)


def login_view(request):
    return render(request, 'home/login.html')


def register_view(request):
    return render(request, 'home/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def add_post(request):
    try:
        if request.method == "POST":
            form = BlogForm(request.POST, request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')

            description = request.POST.get('description')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            post_obj = BlogModel.objects.create(
                user=user,
                title=title,
                description=description,
                image=image,
                content=content
            )

            return redirect('/')
        else:
            form = BlogForm()
    except Exception as e:
        print(e)
    context = {
        'form': form
    }
    return render(request, 'home/add_post.html', context)


def post_detail(request, slug):
    try:
        post = BlogModel.objects.filter(slug=slug).first()
        allcomments = post.comments.filter(status=True)

        post.viewed += 1
        post.save()
    except Exception as e:
        print(e)

    context = {
        'post': post,
        'allcomments': allcomments
    }

    return render(request, 'home/post_detail.html', context)


@login_required
def user_posts(request):
    try:
        posts = BlogModel.objects.filter(
            user=request.user).order_by('-updated_at')
    except Exception as e:
        print(e)

    context = {
        'posts': posts
    }

    return render(request, 'home/user_posts.html', context)


@login_required
def post_update(request, slug):
    try:
        post = BlogModel.objects.filter(slug=slug).first()
        form = BlogForm(initial={'content': post.content})

        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES,
                            initial={'content': post.content})
            image = request.FILES['image']
            title = request.POST.get('title')
            description = request.POST.get('description')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']
                featured = form.cleaned_data['featured']

            post.title = title
            post.description = description
            post.image = image
            post.featured = featured
            post.content = content

            if post.user != request.user:
                return redirect('/')

            post.save()

            return redirect('post_detail', slug=post.slug)

    except Exception as e:
        print(e)

    context = {
        'post': post,
        'form': form
    }

    return render(request, 'home/update_post.html', context)


@login_required
def post_delete(request, id):
    try:
        post = BlogModel.objects.get(id=id)
        if post.user == request.user:
            post.delete()

    except Exception as e:
        print(e)

    return redirect('user_posts')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()

        return redirect('/login')
    except Exception as e:
        print(e)

    return redirect('/')
