from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# docker compose exec web python manage.py makemigrations
# docker compose exec web python manage.py migrate


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
    title = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photo/%Y/%M/%d/", null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,unique=False)

    video_url = models.URLField(max_length=300, null=True, blank=True)
    video_embed_url = models.URLField(max_length=300, null=True, blank=True)
    # lvl_user=models.IntegerField(max_length=1,blank=False,null=False,default=0)
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # 0 - гість/читач, 1 - адмін, 2 - модератор, 3 - автор, ... (приклад)
    lvl_user = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(9)]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(lvl_user__gte=0, lvl_user__lte=9),
                                name="profile_lvl_user_between_0_9")
        ]

    def __str__(self):
        return f"{self.user.username} (lvl {self.lvl_user})"