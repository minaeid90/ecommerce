from django.db import models
from django.db.models.signals import pre_save

from ecommerce.utils import unique_slug_generator


class Post(models.Model):

    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('blog:detail', kwargs={'pk': self.pk})


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
