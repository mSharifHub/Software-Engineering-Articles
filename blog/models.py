from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.core.validators import MinLengthValidator


class Post(models.Model):
    slug = models.SlugField(default="", null=False, blank=True, unique=True, db_index=True)
    image = models.ImageField(upload_to='blog/images/')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    content = models.TextField(validators=[MinLengthValidator(10)])
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)

    class Meta:
        verbose_name = "Blog Post"

    def get_absolute_url(self):
        return reverse("post-detail-page", args=[self.slug])

    def post_info(self):
        return f"{self.title} by {self.author} on {self.date}"

    def __str__(self):
        return self.post_info()

