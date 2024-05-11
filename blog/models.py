from django.db import models
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Post(models.Model):
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blog/images/')
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True)

    def __str__(self):
        return f"{self.title}\n{self.image}\n{self.date}\n{self.author}\n{self.slug}\n{self.content}\n{self.rating}"
