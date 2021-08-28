import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from .forms import BlogForm
from .models import BlogModel, Like, Profile


class Home(ListView):
    template_name = 'home/home.html'
    queryset = BlogModel.objects.all()
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(is_draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['featured_post'] = BlogModel.objects.filter(
            featured=True).last()

        return context


def login_view(request):
    return render(request, 'home/login.html')


def register_view(request):
    return render(request, 'home/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


class AddPost(LoginRequiredMixin, FormView):
    form_class = BlogForm
    template_name = 'home/add_post.html'
    success_url = '/'

    def form_valid(self, form):
        form_cd = form.cleaned_data
        data = self.request.POST
        form.save(commit=False)

        post_obj = BlogModel.objects.create(
            user=self.request.user,
            title=data['title'],
            description=data['description'],
            image=self.request.FILES['image'],
            content=form_cd['content'],
            is_draft=form_cd['is_draft'],
            featured=form_cd['featured']
        )

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print('Form is invalid!')


def post_detail(request, slug):
    try:
        post = BlogModel.objects.filter(slug=slug).first()

        allcomments = post.comments.filter(status=True)

        post.viewed += 1
        post.save()

        likes = post.likes.filter(created_by__id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False

    except Exception as e:
        print(e)

    context = {
        'post': post,
        'allcomments': allcomments,
    }

    return render(request, 'home/post_detail.html', context)


class UserPosts(LoginRequiredMixin, ListView):
    template_name = 'home/user_posts.html'
    context_object_name = 'posts'
    queryset = BlogModel.objects.all()
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(user=self.request.user)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = BlogForm
    template_name = 'home/update_post.html'
    queryset = BlogModel.objects.all()
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        form_cd = form.cleaned_data
        data = self.request.POST
        post_obj = self.get_object()

        post_obj.title = data['title']
        post_obj.description = data['description']
        post_obj.image = self.request.FILES['image']
        post_obj.featured = form_cd['featured']
        post_obj.is_draft = form_cd['is_draft']
        post_obj.content = form_cd['content']

        if post_obj.user != self.request.user:
            return redirect('/')

        post_obj.save()

        return HttpResponseRedirect(post_obj.get_absolute_url())

    def form_invalid(self, form):
        print('Form is invalid!')


class PostDelete(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = 'id'
    model = BlogModel
    success_url = '/'
    template_name = 'home/post_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(PostDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


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
