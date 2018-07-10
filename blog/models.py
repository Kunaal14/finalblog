from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

from django.core.validators import RegexValidator
# Create your models here.
from django.db.models.signals import pre_save, post_save
USERNAME_REGEX='^[a-zA-Z0-9.@+-]*$'
# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, email,  password=None):
        """
        date_of_birth,
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            #date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,email, password):
        """
        , date_of_birth
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,

            password=password,
            #date_of_birth=date_of_birth,

        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user
class MyUser(AbstractBaseUser):
    #user = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username    =   models.CharField(max_length=225, 
                                         
                                        validators=[
                                            #MinLengthValidator(4),
                                            RegexValidator(
                                                regex = USERNAME_REGEX,
                                                message= 'Username must be Alphanumeric or must contain any of the following:". @ + -"',
                                                code = 'invalid username'
                                                
                                            )],
                                        unique=True,

                                    )
    #name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100,null=True, blank=True)
    zip_code = models.CharField(max_length=120, default="1234")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        return reverse("blog:dashboard", kwargs={"slug": self.slug})


    



class Post(models.Model):
    user = models.ForeignKey(MyUser,  on_delete=models.CASCADE,default=1)
               
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=100, null=True, blank=True,)
    #  
    name = models.CharField(max_length=100, null=True, blank=True)        
    
            
    # height_field = models.IntegerField(default=0)
    # width_field = models.IntegerField(default=0)
    content = models.TextField(null=True, 
             blank=True,)
    # draft = models.BooleanField(default=False )
    # publish = models.DateField( null=True, 
    #         blank=True, auto_now=False, auto_now_add=False)
    # updated = models.DateTimeField( null=True, 
    #         blank=True, auto_now=True, auto_now_add=False)
    # timestamp = models.DateTimeField( null=True, 
    #         blank=True, auto_now=False, auto_now_add=True)

    # #objects = PostManager()

    # def __unicode__(self):
    #     return self.title

    def __str__(self):
        return str(self.user)

    # def get_absolute_url(self):
    #     return reverse("blog:detail", kwargs={"slug": self.slug})

    # class Meta:
    #     ordering = ["-timestamp", "-updated"]
    
# def post_save_user_model_reciever(sender, instance, created, *args, **kwargs):
#     if created:
#         try:
#             Profile.objects.create(user=instance)
#             ActivationProfile.objects.create(user=instance) 
#             # slug = slugify(instance.username)
#             # instance.slug = slug
#         except:
#             pass
# post_save.connect(post_save_user_model_reciever, sender=MyUser)

# def save(self, *args, **kwargs):
#         if not self.slug and self.user:
#             self.slug = slugify(self.user)
#         super(MyUser, self).save(*args, **kwargs)

def pre_save_MyUser(sender, instance,created, *args, **kwargs):
    slug = slugify(instance.user)
    instance.slug = slug
    if created:
        try:
            Profile.objects.create(user=instance)
            ActivationProfile.objects.create(user=instance) 
        except:
            pass

pre_save.connect(pre_save_MyUser, sender=Post)
    

def pre_save_MyUser(sender, instance, *args, **kwargs):
    #username = str(instance.username)
    slug = slugify(instance.username)
    instance.slug = slug
pre_save.connect(pre_save_MyUser, sender=MyUser)


def pre_save_Post(sender, instance, *args, **kwargs):
    #username = str(instance.username)
    slug = slugify(instance.user)
    instance.slug = slug
pre_save.connect(pre_save_Post, sender=Post)