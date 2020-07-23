import os
from django.db import models
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.contrib.contenttypes.fields import GenericRelation
from courses.utils import unique_slug_generator
from django.contrib.contenttypes.models import ContentType 

from star_ratings.models import Rating
from reviews.models import Review


class Category(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self):
        return self.name
    

class Course(models.Model):
    title = models.CharField(max_length=250,blank=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='photos/course/%Y-%m-%d/')
    price = models.DecimalField(max_digits=100, decimal_places=2,null=True,blank=True)
    offer_price =  models.DecimalField(max_digits=100, decimal_places=2,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=50)
    ratings = GenericRelation(Rating, related_query_name='ratings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    instructor = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name='instructor')


    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = "courses"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:single-course", kwargs={'slug': self.slug})
 
    #for review section
    # def get_content_type(self):
    #     return self.get_content_type
        
    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type    


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Course)
  
  

@receiver(models.signals.post_delete, sender=Course)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(models.signals.pre_save, sender=Course)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).thumbnail
    except sender.DoesNotExist:
        return False

    new_file = instance.thumbnail
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    

class LessonContent(models.Model):
    title  = models.CharField(max_length=250, blank=True)
    video_link = models.URLField(max_length=500, blank=False)

    class Meta:
        verbose_name = "Lesson Content"
        verbose_name_plural = "Lessons Contents"
        db_table = "lessonsContents"

    def __str__(self):
        return self.video_link

    @property

    def lesson(self):
        return self.lesson_set.all()

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
    title  = models.CharField(max_length=250, blank=False)
    video_link = models.ManyToManyField(LessonContent)
    # video_link = models.ForeignKey(LessonContent, on_delete=models.CASCADE, related_name='lessoncontent')


    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        db_table = "lessons"

    def __str__(self):
        return self.title
