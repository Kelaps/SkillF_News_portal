from tkinter.colorchooser import Chooser
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """автор наследует от User. каскадное удаление"""
    rating = models.IntegerField(default=0)

def update_rating(self, rating_to_update):      
    # Подсчет рейтинга постов пользователя.
    list_rating_of_posts = Post.objects.filter(post_author=self.user).values('rating')
    sum_rating_of_posts = 0
    for i in range(len(list_rating_of_posts)):
        sum_rating_of_posts += i.rating
    sum_rating_of_posts = sum_rating_of_posts * 3


    # Подсчет рейтинга комментариев пользователя.
    list_rating_of_comments = Comment.objects.filter(comment_user=self.user).values('rating_comment')
    sum_rating_of_comment = 0
    for y in range(len(list_rating_of_comments)):
        sum_rating_of_comment += y.rating

    
 # Подсчет рейтинга комментариев к статьям пользователя
    list_rating_of_post_comments = Comment.objects.filter(comment_post__post_author=self.user).values('rating_comment')
    sum_rating_of_post_comments = 0
    for w in range(len(list_rating_of_post_comments)):
        sum_rating_of_post_comments += w.rating

 # Подсчет общего рейтинга
    rating_to_update = sum_rating_of_posts + sum_rating_of_comment + sum_rating_of_post_comments



class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    article = 'ar'
    news = 'ne'
    article_or_news = [
        (article, 'Статья'), 
        (news, 'Новости') 
    ]

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE) #один ко многим
    post_date = models.DateTimeField(auto_now_add=True)
    choose = models.CharField(max_length=2, choices=article_or_news)   # поле с выбором — «статья» или «новость»
    post_category = models.ManyToManyField(Category)
    liked_by = models.ManyToManyField(User, related_name="liked_posts") 
    title = models.CharField(max_length=60)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    def prview(self):
        return self.text[:124] + "..."

    def like(self):
        self.rating_post += 1
        self.save()
        
    def dislike(self):
        self.rating_post -= 1
        self.save()


class PostCategory(models.Model):
    post_rel = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_rel = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    comment_date = models.DateTimeField( null=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()
        
    def dislike(self):
        self.rating_comment -= 1
        self.save()




