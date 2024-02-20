from django.contrib import admin
from .models import CustomUser
admin.site.register(CustomUser)



from django.contrib import admin
from .models import OrderedProduct

admin.site.register(OrderedProduct)
