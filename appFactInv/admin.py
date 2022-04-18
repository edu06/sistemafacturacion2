from django.contrib import admin
from appFactInv.models import personas,proveedores,telefonos_personas,detalle_productos,perfiles_colaboradores
from appFactInv.models import productos,encabezado_factura,detalle_factura,marcas,regimens,unidad_medidas

from django.forms import TextInput, Textarea
from django.db import models


admin.site.register(personas)
admin.site.register(proveedores)
admin.site.register(telefonos_personas)
admin.site.register(detalle_productos)
admin.site.register(productos)
admin.site.register(encabezado_factura)
admin.site.register(detalle_factura)
admin.site.register(marcas)
admin.site.register(regimens)
admin.site.register(unidad_medidas)
admin.site.register(perfiles_colaboradores)

class YourModelAdmin(admin.ModelAdmin):
 formfield_overrides = {
  models.CharField: {'widget': TextInput(attrs={'size':'20'})},
  models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
 }

