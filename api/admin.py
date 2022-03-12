from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Report)
admin.site.register(Order)
admin.site.register(OrderItem)
