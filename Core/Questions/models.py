from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.template.defaultfilters import slugify
import time
import threading

# Create your models here.


# Answer 1

class MyBlog(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)


@receiver(pre_save, sender=MyBlog)
def my_blog_pre_save(sender, instance, *args, **kwarsg):
    print("Signal received for make slug, processing...")
    if not instance.slug:
        instance.slug = slugify(instance.title)
        time.sleep(10)  # Simulating a long-running task
    print("Signal processing slug making completed.")

    # this will prove django signals executed synchronously



# Answer 2

class MyBlogtwo(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)


@receiver(pre_save, sender=MyBlogtwo)
def my_blog_two_pre_save(sender, instance, *args, **kwarsg):
    print(f"Signal received in thread: {threading.current_thread().name}")
    print("Signal received for make slug, processing...")
    if not instance.slug:
        instance.slug = slugify(instance.title)
        print(f"Slug created, thread: {threading.current_thread().name}")
    else:
        count = 0
        while (count < 10):
            count = count + 1
            print(f"Slug already present, count: {count}, thread: {threading.current_thread().name}")
    print("Signal processing slug making completed.")

    # this will prove django signals runs in same thread


# Answer 3

class MyBlogthree(models.Model):
    title = models.CharField(max_length=50)
    is_publish = models.BooleanField(default=False)


@receiver(post_save, sender=MyBlogthree)
def my_blog_three_pre_save(sender, instance, *args, **kwarsg):
    print("Signal received pls wait we are changing the title, processing...")
    if not instance.is_publish:
        instance.is_publish = True
        instance.title = f"This is published article - {instance.title}"
        instance.save()
    print("Signal processing changing title completed.")

    # when we try to save our title and publish is false in db this will change it and add prefix 'This is published article - ' and mark publish = True. this will prove django signals run in the same database transaction as the caller