from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class nearestloc(models.Model):
    location = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.location


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


class payment(models.Model):
    nearestloc = models.ForeignKey(nearestloc, on_delete=models.CASCADE, )
    # qty = models.IntegerField()
    # deliveryMode = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField()
    notes = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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




class Admin_log(models.Model):
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.username
