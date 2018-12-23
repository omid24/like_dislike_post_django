from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Post, LikeDislike
from django.views.generic.base import RedirectView
from django.contrib.auth.models import User
from django.views.generic.list import ListView
import json


class PostListView(ListView):

    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'

    # current user when is login
    login_user_id = None
    is_login_user = False

    def get(self, request, *args, **kwargs):
        # current user when is login
        self.login_user_id = request.user.id
        self.is_login_user = request.user.is_authenticated

        return super(PostListView, self).get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        # show like count
        # likes_count = LikeDislike.object.getLikes(post_id=post_id)
        # show dislike count
        if request.method == 'POST':
            if request.user.is_authenticated:
                if request.POST.get('action'):
                    post_id = request.POST.get('post_id')
                    user_id = request.POST.get('user_id')
                    action = request.POST.get('action')

                    if action == 'like':
                        LikeDislike.objects.update_or_create_like(post_id, user_id)

                    elif action == 'unlike':
                        LikeDislike.objects.delete_after_unlike(post_id, user_id)

                    elif action == 'dislike':
                        LikeDislike.objects.update_or_create_dislike(post_id, user_id)

                    elif action == 'undislike':
                        LikeDislike.objects.delete_after_undislike(post_id, user_id)
                    else:
                        return None

                    # Post.objects.get_rating_by_ajax(post_id)
                    # store count like and dislike
                    count_likes     = LikeDislike.objects.filter(post__id=post_id, rating_action=1).count()
                    count_dislikes  = LikeDislike.objects.filter(post__id=post_id, rating_action=0).count()

                    # rating.dict(count_likes=count_likes, count_dislikes=count_dislikes)
                    return JsonResponse({
                        'likes': count_likes,
                        'dislikes': count_dislikes
                    })
            else:
                return redirect('post_url')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_login_user'] = self.is_login_user

        if self.login_user_id is not None:
            context['login_user_id'] = self.login_user_id

        return context
