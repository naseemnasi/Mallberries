from django.contrib import admin
from app1.models import Register,Category, product, Admin_log, Order

# Register your models here.

admin.site.register(Register)
# admin.site.register(Order)
# admin.site.register(Landmark)



class catAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(Category, catAdmin)


class proAdmin(admin.ModelAdmin):
    list_display = ("pname","id", "price","category", "stock")


admin.site.register(product, proAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "date")


admin.site.register(Order, OrderAdmin)
admin.site.register(Admin_log)
