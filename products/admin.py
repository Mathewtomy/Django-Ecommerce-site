from django.contrib import admin

# Register your models here.
from .models import Product,Category,Customer,Order,Return,Product_Category,Product_option,Product_option_name,Banner,Product_option_description,Blog,CartItem
from .models import Contact,About
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','stock')
    prepopulated_fields = {"slug": ("name",)}
    
    
admin.site.register(Product,ProductAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','address','phone')
    
    
admin.site.register(Contact,ContactAdmin)

class AboutAdmin(admin.ModelAdmin):
    list_display=('name')
    
class BlogAdmin(admin.ModelAdmin):
    list_display=('name','blog','image')
        
# admin.site.register(About,AboutAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=['category_name']
    
class StatusAdmin(admin.ModelAdmin):
    list_display=['product_status']

class Product_OptionAdmin(admin.ModelAdmin):
    list_display=['option']

class Product_Option_NameAdmin(admin.ModelAdmin):
    list_display=['option_name']

class BannerAdmin(admin.ModelAdmin):
    list_display=['name','image']
class Product_descriptionAdmin(admin.ModelAdmin):
    list_display=['product','product_option','product_option_name']
    
class Cart_itemAdmin(admin.ModelAdmin):
    list_display=['session','product','customer','quantity','date_added ']
        
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Return)
admin.site.register(About)
admin.site.register(Product_Category)
admin.site.register(Product_option)
admin.site.register(Product_option_name)
admin.site.register(Banner)
admin.site.register(Product_option_description)
admin.site.register(Blog)
admin.site.register(CartItem)