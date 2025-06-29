from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорії'
        verbose_name_plural = "Категорії"


class TagPost(models.Model):
    tag = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class library(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, db_index=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photo/%Y/%M/%d/", null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,unique=False)

    video_url = models.URLField(max_length=300, null=True, blank=True)
    video_embed_url = models.URLField(max_length=300, null=True, blank=True)

    tags = models.ManyToManyField('TagPost', blank=True, related_name="tags")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Відома бібліотека'
        verbose_name_plural = 'Відомі бібліотеки'
        ordering = ['time_create', 'time_update']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    @property
    def video_id(self):

        if self.video_url:
            if 'youtu.be/' in self.video_url:
                return self.video_url.split('/')[-1].split('?')[0]
            elif 'v=' in self.video_url:
                return self.video_url.split('v=')[-1].split('&')[0]
        return None

    def save(self, *args, **kwargs):

        if self.video_id:
            self.video_embed_url = f"https://www.youtube.com/embed/{self.video_id}"
        else:
            self.video_embed_url = None
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes

    def total_dislikes(self):
        return self.dislikes


class Reaction(models.Model):
    LIKE = 'L'
    DISLIKE = 'D'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(library, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=1, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.reaction} - {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey('library', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    unapproved = models.BooleanField(default=False)

    def __str__(self):
        return self.text
