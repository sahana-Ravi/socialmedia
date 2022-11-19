from django.urls import path 
from .views import PostListView, PostDetailView,PostEditView, PostDeleteView, CommentDeleteView, ProfileView,ProfileEditView,AddFollowers,RemoveFollowers, AddLike, DisLike,UserSearch
urlpatterns =[
    path('',PostListView.as_view(),name='post-list'),
    path('post/<int:pk>/like',AddLike.as_view(),name='like'),
    path('post/<int:pk>/dislike',DisLike.as_view(),name='dislike'),
    path('post/<int:pk>',PostDetailView.as_view(),name='post-detail'),
    path('post/edit/<int:pk>',PostEditView.as_view(),name='post-edit'),
    path('post/delete/<int:pk>',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>', CommentDeleteView.as_view(),name='comment-delete'),
    path('profile/<int:pk>',ProfileView.as_view(),name='profile'),
    path('profile/edit/<int:pk>',ProfileEditView.as_view(),name='profile-edit'),
    path('profile/<int:pk>/followers/add',AddFollowers.as_view(),name='add-follower'),
    path('profile/<int:pk>/followers/remove',RemoveFollowers.as_view(),name='remove-follower'),
    path('search/',UserSearch.as_view(), name='profile-search'),




]