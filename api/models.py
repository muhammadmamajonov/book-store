from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManger(BaseUserManager):

    def create_superuser(self, phone, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("Superuser is_staff=True bo'lishi shart")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("Superuser is_superuser=True bo'lishi shart")
        
        return self.create_user(phone, password, **other_fields)

    def create_user(self, phone, password, **other_fields):
        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='pictures/book-pictures')
    author = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_year = models.CharField(max_length=4)
    description = models.TextField()
    price = models.FloatField(default=0)
    discount_price = models.FloatField(null=True, blank=True)
    discount_expiration = models.DateField(null=True, blank=True)
    quantity = models.IntegerField()
    sold_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name



class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=17, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    purchased_books = models.ManyToManyField(Book, null=True, blank=True)

    objects = UserManger()
    USERNAME_FIELD = 'phone'

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.IntegerField()


class Report(models.Model):
    user = models.CharField(max_length=50)
    did = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    item_price = models.FloatField()

    def __str__(self):
        return f"{self.book.name}|{self.date_added}"


class Order(models.Model):
    STATUS = (
        ('open', 'open'),
        ('receive', 'receive'),
        ('received', 'received')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(OrderItem, null=True, blank=True)
    total_price = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=STATUS, default='open')