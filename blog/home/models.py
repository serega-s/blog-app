from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from mptt.models import MPTTModel, TreeForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)


class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    content = FroalaField()
    slug = models.SlugField(max_length=255, blank=True, null=True)
    image = models.ImageField()
    featured = models.BooleanField(default=False)
    viewed = models.IntegerField(default=0)
    is_draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        from .helpers import generate_slug
        self.slug = generate_slug(self.title)
        super(BlogModel, self).save(*args, **kwargs)


class Comment(MPTTModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    post = models.ForeignKey(BlogModel, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            blank=True, null=True, related_name='children')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self) -> str:
        return self.user.username
