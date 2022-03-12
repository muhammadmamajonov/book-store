
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('auth', UserViewset)
router.register('book', BookViewset)
router.register('category', CategoryViewset)
router.register('order', OrderViewset)