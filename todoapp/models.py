from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from django.urls import reverse


class TodoCategory(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

    class Meta:
        ordering = ('-date',)


class Todo(models.Model):
    title = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.BooleanField(default=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey('TodoCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo_detail', args=[str(self.id)])

    class Meta:
        ordering = ('-created_date',)
