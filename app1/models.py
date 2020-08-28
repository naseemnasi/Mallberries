import _datetime
from datetime import datetime

from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.name

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Register.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Register.objects.filter(email=self.email):
            return True

        return False



class product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, )
    pname = models.CharField(max_length=255)
    pimage = models.ImageField(null=True, blank=True)
    pdesc = models.CharField(max_length=2083)
    price = models.IntegerField()
    size = models.CharField(max_length=40, blank=True)
    stock = models.IntegerField()



    def __str__(self):
        return self.pname

    @staticmethod
    def get_products_by_id(ids):
        return product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_prd():
        return product.objects.all()

    @staticmethod
    def get_all_prd_by_id(prd_id):
        if prd_id:
            return product.objects.filter(id=prd_id)
        else:
            pass;

    @staticmethod
    def get_all_prd_by_categoryID(category_id):
        if category_id:
            return product.objects.filter(category=category_id)
        else:
            return product.get_all_prd();

    @staticmethod
    def get_products_id(ids):
        return product.objects.filter(id__in =ids )

#
# class Landmark(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name


class Order(models.Model):
    product = models.ForeignKey(product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Register,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)
    # location = models.ForeignKey(Landmark,on_delete=models.CASCADE, )

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id)


class Admin_log(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.username
