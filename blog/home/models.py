from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from mptt.models import MPTTModel, TreeForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.user.username


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

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.title)

            has_slug = BlogModel.objects.filter(slug=slug).exists()
            count = 1

            while has_slug:
                count += 1
                slug = slugify(self.title) + '-' + str(count)
                has_slug = BlogModel.objects.filter(slug=slug).exists()

            self.slug = slug
        super(BlogModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})


class Comment(MPTTModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    post = models.ForeignKey(
        BlogModel, on_delete=models.CASCADE, related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            blank=True, null=True, related_name='children')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self) -> str:
        return self.user.username


class Like(models.Model):
    post = models.ForeignKey(
        BlogModel, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.post.title}'
