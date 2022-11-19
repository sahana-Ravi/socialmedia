from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView,DeleteView


# Create your views here.
class PostListView(LoginRequiredMixin,View):
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        posts=Post.objects.all().order_by('created_on')
        form= PostForm()

        context = {
            'post_list':posts,
            'form':form,
        }
        return render(request,'social/post_list.html',context) 
    
    def post(self, request, *args, **kwargs):
        
        posts=Post.objects.all().order_by('created_on')
        form = PostForm(request.POST)

        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.save() 
            
        context = {
            'post_list':posts,
            'form':form,
        }
        return render(request,'social/post_list.html',context) 
class PostDetailView(LoginRequiredMixin,View):
    @csrf_exempt
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk) 
        form = CommentForm()
        comments= Comment.objects.filter(post=post).order_by('created_on')
        context={
            'post':post,
            'form':form,
            'comments':comments
        }
        return render(request, 'social/post_details.html',context) 
    def post(self, request, pk , *args, **kwargs):
        post = Post.objects.get(pk=pk) 
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.post=post 
            new_comment.save()
        comments= Comment.objects.filter(post=post).order_by('created_on')
        context={
            'post':post,
            'form':form,
            'comments':comments
        }
        return render(request, 'social/post_details.html',context) 
    
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post 
    fields = ['body']
    template_name='social/post_edit.html'
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('post-detail',kwargs={'pk':pk})
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model=Post 
    template_name= 'social/post_delete.html'
    success_url= reverse_lazy('post-list') 
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model= Comment
    template_name= 'social/comment_delete.html'
   
    def get_success_url(self):
        pk=self.kwargs['post_pk']
        return reverse_lazy('post-detail',kwargs={'pk':pk})
    def test_func(self):
        post=self.get_object()
        return self.request.user == post.author
    
class ProfileView(View):
    def get(self, request , pk, *args , **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user 
        posts = Post.objects.filter(author=user).order_by('created_on')
        followers = profile.followers.all()
        if len(followers)==0:
            is_following=False
        for follower in followers:
            if follower==request.user:
                is_following= True
                break 
            else:
                is_following= False
        number_of_followers= len(followers)
        context = {
            'user':user,
            'profile': profile,
            'posts': posts,
            'number_of_followers':number_of_followers,
            'is_following': is_following,
        } 
        return render(request, 'social/profile.html',context)   
class ProfileEditView(LoginRequiredMixin,UserPassesTestMixin, UpdateView ):
    model = UserProfile
    fields= ['name', 'bio', 'birth_date','location', 'picture']
    template_name = 'social/profile_edit.html'
    def get_success_url(self):
        pk=self.kwargs['pk']
        return reverse_lazy('profile',kwargs={'pk':pk})
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
class AddFollowers(LoginRequiredMixin,View):
    def post(self,request, pk , *args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        return redirect('profile', pk=profile.pk)
class RemoveFollowers(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile=UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return redirect('profile', pk=profile.pk) 
class AddLike(LoginRequiredMixin, View):
    def post(self,request, pk, *args,**kwargs ):
        is_dislike=False
        post = Post.objects.get(pk=pk)
        for dislike in post.dislikes.all():
            if dislike==request.user:
                is_dislike=True 
                break 
        if is_dislike:
            post.dislikes.remove(request.user)
        is_like=False
        post = Post.objects.get(pk=pk)
        for like in post.likes.all():
            if like==request.user:
                is_like=True 
                break 
        if not is_like:
            post.likes.add(request.user)
        if is_like:
            post.likes.remove(request.user) 
        next=request.POST.get('next', '/')
        return HttpResponseRedirect(next)
class DisLike(LoginRequiredMixin, View):
      def post(self,request, pk, *args,**kwargs ):
        is_like=False
        post = Post.objects.get(pk=pk)
        for like in post.likes.all():
            if like==request.user:
                is_like=True 
                break 
        if is_like:
            post.likes.remove(request.user)
        is_dislike=False
        post = Post.objects.get(pk=pk)
        for dislike in post.dislikes.all():
            if dislike==request.user:
                is_dislike=True 
                break 
        if not is_dislike:
            post.dislikes.add(request.user)
        if is_dislike:
            post.likes.remove(request.user)
        next=request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = ''
        if query:
            profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
            ) 
        print(query)
        context = {
            'profile_list': profile_list,
           }

        return render(request, 'social/search.html', context)