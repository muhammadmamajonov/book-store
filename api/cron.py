from datetime import datetime
from django.core.mail import send_mail
import requests
# import os
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
# django.setup()
TOKEN = '2020316126:AAGznP4Hx6DC02stEPktvmx9b5m9_NWQel4'

# from api.models import User
def send_report():

    text = "Assalomu alaykum hurmatli foydalanuvchi Botimiz sizga foydasi tegayotgan bo'lsa biz bundan mamnunmiz"
    res = requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={859264113}&text={text}")
        # admin.email for admin in User.objects.filter(is_superuser=True)
    email = send_mail(
        'weekly report',
        'weekly sales report',
        'muhammadbekmamajonov@gmail.com',
        ['muhammadyusufbek1998@gmail.com'],
        fail_silently=False,
    )
    # email.send()
send_report()