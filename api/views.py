from re import M
from string import punctuation
from unicodedata import category
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib import auth
from django.db.models import Q
from .serializers import *
from .models import *

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False)
    def signup(self, request):
        data = request.data
        
        phone = data['phone']
        password1 = data['password1']
        password2 = data['password2']
        first_name = data['first_name']
        last_name = data['last_name']
        address = data['address']

        try:
            User.objects.get(phone=phone)
            return Response({'message':"this phone is already registered"})
        except:
            if password1==password2:
                user = User.objects.create_user(phone=phone, password=password1, first_name=first_name, last_name=last_name, address=address)
                token = Token.objects.create(user=user)
                data = {
                    'id':user.id,
                    'phone':user.phone,
                    'first_name':user.first_name,
                    'last_name':user.last_name,
                    'address':user.address,
                    'token':token.key
                }
                return Response(data, status=201)
            else:
                return Response({'message':"passwords not matching"})

    @action(methods=['post'], detail=False)
    def signin(self, request):
        data = request.data

        phone = data['phone']
        password = data['password']

        
        user = auth.authenticate(phone=phone, password=password)

        if user is not None:
            data = {
                'id':user.id,
                'phone':user.phone,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'address':user.address,
                'is_staff':user.is_staff,
                'is_superuser':user.is_superuser,
                'token':Token.objects.get(user=user).key
            }
            return Response(data, status=200)
        
    
        return Response({'message':"Phone number or password is incorrect"})



class BookViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(methods=['post'], detail=False)
    def add_new(self, request):
        data = request.data
        
        user_id = data['user_id']
        name = data['name']
        author = data['author']
        publish_year = data['publish_year']
        price = data['price']
        quantity = data['quantity']
        description = data['description']
        category_id = data['category_id']
        picture = request.FILES['picture']

        book = Book.objects.create(name=name, author=author, publish_year=publish_year,
                                   price=price, quantity=quantity, description=description,
                                   category_id=category_id, picture=picture)

        user = User.objects.get(id=user_id)
        Report.objects.create(user=user.get_full_name(), did=f"{book.name} nomli kitob qo'shdi")
        serialized = self.get_serializer_class()(book)

        return Response(serialized.data, status=201)

    @action(methods=['post'], detail=False)
    def add_quantity(self, request):
        data = request.data

        user_id = data['user_id']
        book_id = data['book_id']
        quantity = data['quantity']

        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        book.quantity += int(quantity)
        book.save()

        Report.objects.create(user=user.get_full_name(), did=f"{book.name} kitob miqdorini {quantity} ga oshirdi")

        return Response({'message':"quantity increased"}, status=200)

    @action(methods=['post'], detail=False)   
    def set_discount(self, request):
        data = request.data

        user_id = data['user_id']
        book_id = data['book_id']
        discount_price = data['discount_price']
        discount_expiration = data['discount_expiration']

        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        book.discount_price = discount_price
        book.discount_expiration = discount_expiration
        book.save()

        Report.objects.create(user=user.get_full_name(), did=f"{book.name} kitobining narxini {discount_expiration} gacha {discount_price} qilib belgiladi")

        return Response({'message':'discount is set'}, status=200)
        
    @action(methods=['get'], detail=False) 
    def search(self, request):
        data = request.GET
        name = data.get('name')
        author = data.get('author')
        
        if name and author:
            books = Book.objects.filter(Q(name__contains=name) | Q(author__icontains=author))
        elif name:
            books = Book.objects.filter(name__icontains=name)
        elif author:
            books = Book.objects.filter(author__icontains=author)
        else:
            return Response({'message':'Kitob nomi yoki muallifini kiriting'})
        serialized = self.get_serializer_class()(books, many=True)

        return Response(serialized.data, status=200)

    @action(methods=['get'], detail=False) 
    def filter(self, request):
        data = request.GET
        category_id = data.get('category_id')

        books = Book.objects.filter(category_id=category_id)
        serialized = self.get_serializer_class()(books, many=True)

        return Response(serialized.data, status=200)
    

class CategoryViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['post'], detail=False)
    def add_new(self, request):
        
        name = request.data['name']
        user_id = request.data['user_id']
        category = Category.objects.create(name=name)

        user = User.objects.get(id=user_id)
        Report.objects.create(user=user.get_full_name(), did=f"{category.name} nomli kategoriya qo'shdi")
        
        serialized = self.get_serializer_class()(category)

        return Response(serialized.data, status=201)


class OrderViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    @action(methods=['get'], detail=False)
    def get_open_order(self, request):
        user_id = request.GET['user_id']
        order = Order.objects.filter(user_id=user_id, status='open').first()
        if order:
            serialized = self.get_serializer_class()(order)
            return Response(serialized.data, status=200)
        return Response({'message':"There is no open order"})


    @action(methods=['post'], detail=False)
    def add(self, request):
        data = request.data

        user_id = data['user_id']
        book_id = data['book_id']
        item_price = data['item_price']

        book = Book.objects.get(id=book_id)
        order_item = OrderItem.objects.create(book_id=book_id, item_price=item_price)
        order = Order.objects.filter(user_id=user_id, status='open').first()

        if order:
            order.items.add(order_item)
            order.total_price += int(item_price)
            order.save()
            book.quantity -= 1
            book.save()
            return Response({'message':'add this book to order'}, status=200)

        order = Order.objects.create(user_id=user_id)
        order.items.add(order_item)
        order.total_price += int(item_price)
        order.save()
        book.quantity -= 1
        book.save()
        return Response({'message':'create new order and add this book to order'}, status=200)
    
    @action(methods=['post'], detail=False)
    def change_quantity(self, request):
        data = request.data

        item_id = data['item_id']
        quantity = int(data['quantity'])
        item_price = float(data['item_price'])

        item = OrderItem.objects.get(id=item_id)
        difference = quantity - item.quantity

        item.quantity = quantity
        order = item.order_set.all().first()
        order.total_price += item_price - item.item_price
        order.save()
        item.item_price = item_price
        item.save()

        book = item.book
        book.quantity -= difference
        book.save()

        return Response({'message':"quantity changed"}, status=200)


    @action(methods=['delete'], detail=False)    
    def remove_item(self, request):
        item_id = request.data['item_id']
        
        item = OrderItem.objects.get(id=item_id)
        order = item.order_set.all().first()
        order.total_price -= item.item_price
        order.save() 

        book = item.book
        book.quantity += item.quantity
        book.save()
        
        item.delete()
        return Response({'message':'Item deleted'}, status=200)

    @action(methods=['post'], detail=False)
    def change_status(self, request):
        data = request.data

        status = data ['status']
        order_id = data['order_id']
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        user = order.user

        if status == 'receive':
            for item in order.items.all():
                book = item.book
                book.sold_quantity += item.quantity
                book.save()
                user.purchased_books.add(book)
                user.save()
                
            return Response({'message':'set receive'}) 
        
        return Response({'message':'set received'})
            

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        data = request.data

        order_id = data['order_id']
        order = Order.objects.get(id=order_id)

        for item in order.items.all():
                book = item.book
                book.quantity += item.quantity
                book.save()   
                order.delete() 

        return Response({'message':'Order deleted'})  