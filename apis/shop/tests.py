from django.test import TestCase
from apis.shop.models import Product

# Create your tests here.

class Product(TestCase):
    fixtures = ['products.json']