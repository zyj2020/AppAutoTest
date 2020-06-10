from django.contrib import admin
from projectMode.models import ProjectMode, ProductMode, DBConfigMode


# Register your models here.


# class ProductModeAdmin(admin.ModelAdmin):
#     list_display = ['productName', 'productFlag', 'productTag',  'productModule', 'id']

class ProjectModeAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'productId':
            try:
                kwargs['queryset'] = ProductMode.objects.filter(productFlag=True)
            except(ValueError, TypeError):
                pass
        return super(ProjectModeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    #  def save_model(self, request, obj, form, change):
    #     try:
    #         product_Id = request.GET.get('productId')
    #         obj.productId = product_Id
    #     except(ValueError, TypeError):
    #         pass
    #     super(ProjectModeAdmin, self).save_model(request, obj, form, change)


admin.site.register(DBConfigMode)
admin.site.register(ProjectMode, ProjectModeAdmin)
admin.site.register(ProductMode)
