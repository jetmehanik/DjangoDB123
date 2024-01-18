from django.db import models
from django.contrib.auth.models import User
import datetime

NEWS = 'NW'
ARTICLE = 'AR'

ONE_CATEGORY = (
    (ARTICLE, 'Статья'),
    (NEWS, 'Новость')
)


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        author_posts_rate = 0
        author_comment_rate = 0
        author_postcom_rate = 0

        author_posts = Post.objects.filter(author=self)
        for p in author_posts:
            author_posts_rate += p.rateOfPost
        author_comment = Comment.objects.filter(_user=self.authorUser)
        for c in author_comment:
            author_comment_rate += c.rateOfComment
        author_postcom = Comment.objects.filter(_post__author=self)
        for pc in author_postcom:
            author_postcom_rate += pc.rateOfComment
        self.rating = author_posts_rate * 3 + author_comment_rate + author_postcom_rate
        self.save()
class Category(models.Model):
    categoryName = models.CharField(max_length=255, unique= True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryTypeChoice = models.CharField (max_length=2, choices=ONE_CATEGORY, default=NEWS)
    dateCreate = models.DateTimeField(auto_now_add= True)
    postCategories = models.ManyToManyField (Category, through='PostCategory')
    nameOfPost = models.CharField (max_length=255, default='New Post')
    textOfPost = models.TextField ()
    rateOfPost = models.IntegerField (default=0)

    def like(self):
        self.rateOfPost += 1
        self.save()

    def dislike (self):
        self.rateOfPost -= 1
        self.save()

    def preview(self):
        return self.textOfPost()[:124]


class PostCategory(models.Model):
    post = models.ForeignKey (Post, on_delete=models.CASCADE)
    category = models.ForeignKey (Category, on_delete=models.CASCADE)


class Comment(models.Model):
    _post = models.ForeignKey (Post, on_delete=models.CASCADE)
    _user = models.ForeignKey (User, on_delete=models.CASCADE)
    comment = models.CharField (max_length= 255)
    dateOfComment = models.DateTimeField (auto_now_add= True)
    rateOfComment = models.IntegerField (default=0)

    def like(self):
        self.rateOfComment += 1
        self.save()

    def dislike (self):
        self.rateOfComment -= 1
        self.save()
