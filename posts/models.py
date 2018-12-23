from django.db import models
from django.contrib.auth.models import User
from cuser.middleware import CuserMiddleware
import json
# from django.contrib import auth


class PostManager(models.Manager):

    # def get_rating_by_ajax(post_id=None):
    #
    #     rating = {} # store count like and dislike
    #
    #     count_likes     = LikeDislike.objects.filter(post__id=post_id, rating_action=1).count()
    #     count_dislikes  = LikeDislike.objects.filter(post__id=post_id, rating_action=0).count()
    #
    #     rating.dict(count_likes=count_likes, count_dislikes=count_dislikes)
    #
    #     return json.dumps(rating)
    pass



# Create your models here.
class Post(models.Model):

    title       = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.title


    @property
    def getLikeCount(self):
        """
        select * from like_dislike, post where
        like_dislike.rating_action = 1 and
        post.id = post.id
        """
        return LikeDislike.objects.filter(rating_action=1, post__id=self.id).count()

    @property
    def getDislikeCount(self):
        """
        select * from like_dislike, post where
        like_dislike.rating_action = 1 and
        post.id = post.id
        """
        return LikeDislike.objects.filter(rating_action=0, post__id=self.id).count()

    @property
    def getLikedUser(self):

        user = CuserMiddleware.get_user()
        # current_user = auth.get_user(request) => for view
        """
        select * from like_dislike, post where
        like_dislike.rating_action = 1 and
        post.id = post.id and user.id=user.id
        """
        count_liked = LikeDislike.objects.filter(rating_action=1, user=user, post__id=self.id).count()
        if count_liked >  0:
            return True
        else:
            return False

    @property
    def getDisLikedUser(self):

        user = CuserMiddleware.get_user()
        # current_user = auth.get_user(request) => for view
        """
        select * from like_dislike, post where
        like_dislike.rating_action = 0 and
        post.id = post.id and user.id=user.id
        """

        count_disliked = LikeDislike.objects.filter(rating_action=0, user=user, post__id=self.id).count()
        if count_disliked >  0:
            return True
        else:
            return False


    objects = PostManager()

#----------------------------------
# ------ LikeDislike Model --------
#----------------------------------
class LikeDislikeManager(models.Manager):

    def update_or_create_like(self, post_id, user_id):
        """
        INSERT INTO LikeDislike set
        user_id=user_id,
        post_id=post_id,
        rating_action=1
        ON DUPLICATE KEY UPDATE rating_action = 1
        """
        obj_user = User.objects.get(pk=user_id)
        obj, created = self.get_queryset().update_or_create(
            post_id = post_id,
            user = obj_user,
            defaults = {'rating_action' : 1},
        )

        return obj, created
        # print(obj_user)
        # print(post_id)
        # fields_dict = {
        #     'obj_user': obj_user,
        #     'post_id': post_id
        # }
        #
        # from django.db import connection
        # with connection.cursor() as cursor:
        #     cursor.execute("""INSERT INTO LikeDislike set
        #                     user=%(obj_user)s,
        #                     post_id=%(post_id)s,
        #                     # rating_action=1 ON DUPLICATE KEY UPDATE rating_action = 1""", **fields_dict)


        # from django.db import connection, transaction
        # cursor = connection.cursor()
        # sql = """INSERT INTO LikeDislike set
        #                 user=%(obj_user)s,
        #                 post_id=%(post_id)s,
        #                 rating_action=1 ON DUPLICATE KEY UPDATE rating_action = 1"""
        # cursor.executemany(sql, fields_dict)
        # transaction.commit_unless_managed()


    def update_or_create_dislike(self, post_id, user_id, *args, **kwargs):
        """
        INSERT INTO LikeDislike set
        user_id=user_id,
        post_id=post_id,
        rating_action=0
        ON DUPLICATE KEY UPDATE rating_action = 0
        """
        obj_user = User.objects.get(pk=user_id)
        obj, created = self.get_queryset().update_or_create(
            post_id = post_id,
            user = obj_user,
            defaults = {'rating_action' : 0},
        )
        return obj, created


    def delete_after_unlike(self ,post_id, user_id, *args,**kwargs):
        """
        DELETE FROM LikeDislike WHERE
        user_id=login_user_id,
        post_id=post_id
        """
        obj_user = User.objects.get(pk=user_id)
        self.get_queryset().filter(post_id=post_id, user=obj_user).delete()



    def delete_after_undislike(self, post_id, user_id):
        """
        DELETE FROM LikeDislike WHERE
        user_id=login_user_id,
        post_id=post_id
        """
        obj_user = User.objects.get(pk=user_id)
        self.get_queryset().filter(post_id=post_id, user=obj_user).delete()




class LikeDislike(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_action   = models.CharField(max_length=30)

    def __str__(self):
        return self.post.title + " / " + self.user.username


    class Meta:
        unique_together = ('post', 'user')


    objects = LikeDislikeManager()
