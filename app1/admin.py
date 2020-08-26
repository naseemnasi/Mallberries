from django.contrib import admin
from app1.models import Register,Category, product, Admin_log, Order

# Register your models here.

admin.site.register(Register)
admin.site.register(Order)



class catAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(Category, catAdmin)


class proAdmin(admin.ModelAdmin):
    list_display = ("pname","id", "price","category", "stock")


admin.site.register(product, proAdmin)
admin.site.register(Admin_log)
