from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Files(models.Model):
    file = models.FileField(upload_to='files/', max_length=100)

    def __str__(self):
        return self.file.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/Default_pfp.jpg")
    birthday = models.DateField()
    age = models.IntegerField(editable=False)  # Calculated field
    bio = models.TextField(max_length=200, blank=True)
    cv = models.ManyToManyField(Files, blank=True)
    expired_token = models.CharField(max_length=50,null=True,blank=True)
    expired_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(Profile, self).save(*args, **kwargs)

    def calculate_age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    image = models.ImageField(upload_to="post_pictures/", blank=True)
    likers = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"

    def like_count(self):
        return self.likers.count()
