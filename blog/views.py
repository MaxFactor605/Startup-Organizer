from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.views.generic import View
from .forms import PostForm


def post_detail(request, year, month, slug, parent_template=None):
    post = get_object_or_404(Post, pub_date__year=year, pub_date__month=month, slug__iexact=slug)
    return render(request, 'blog/post_detail.html', context={'post': post, 'parent_template' : parent_template})


class PostCreate(View):
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form_class})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            return render(request, self.template_name, context={'form': bound_form})


class PostList(View):
    def get(self, request, parent_template=None):
        return render(request, 'blog/post_list.html',
                      context={'post_list': Post.objects.all(), 'parent_template' : parent_template})


class PostUpdate(View):
    form_class = PostForm
    model = Post
    template_name = 'blog/post_update.html'

    def get_object(self, year, month, slug):
        post = get_object_or_404(self.model, pub_date__year=year, pub_date__month=month, slug=slug)
        return post

    def get(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        return render(request, self.template_name, context={'form': self.form_class(instance=post), 'post': post})


    def post(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        bound_form = self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            return render(request, self.template_name, context={'form': bound_form, 'post': post})


class PostDelete(View):
    model = Post

    def get_object(self, year, month, slug):
        post = get_object_or_404(self.model, pub_date__year=year, pub_date__month=month, slug=slug)
        return post

    def post(self, request, year, month, slug):
        post = self.get_object(year, month, slug)
        post.delete()
        return redirect('blog_post_list')