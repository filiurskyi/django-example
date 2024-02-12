from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Author(models.Model):
    fullname = models.CharField(max_length=50, null=False, unique=True)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=100)
    description = models.TextField()
    date_modified = models.DateTimeField("date modified", auto_now_add=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, null=False
    )

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    word = models.CharField(max_length=35, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, null=False
    )

    def __str__(self):
        return self.word


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    tags = models.ManyToManyField(Tag, related_name="quotes")
    quote = models.TextField(null=False)
    date_modified = models.DateTimeField("date modified", auto_now_add=True)
    date_created = models.DateTimeField("date created", auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1, null=False
    )

    def __str__(self):
        return self.quote
