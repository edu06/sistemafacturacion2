
from select import select
from django.db import models
from datetime import datetime
from django.forms import model_to_dict
status=[
(1,'Activo'),
(0,'Inactivo'),
]
class personas(models.Model):
    nombre_persona=models.CharField(max_length=60)
    apellido_persona=models.CharField(max_length=60)
    direccion_persona=models.TextField(default='Ciudad')
    nit_persona=models.CharField(max_length=10,default='C/F')
    telefono_persona=models.CharField(null=True,blank=True, max_length=8)
  
    def __str__(self):
          return '%s %s %s %s'%(self.nit_persona,self.nombre_persona, self.apellido_persona, self.direccion_persona)

    def toJSON(self):# toJSON devuelve los datos del modelo en forma de diccionario. 
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['id']

class proveedores(models.Model):
    nombre_proveedor=models.CharField(max_length=60)
    direccion_proveedor=models.TextField()
    telefono_proveedor=models.CharField(max_length=8)
    nit_proveedor=models.CharField( max_length=10)
    prefijo=models.CharField(max_length=4,default="PRV")
    estado_proveedor=models.IntegerField(null=False,blank=False,choices=status,default=1)
    persona_contacto=models.ForeignKey(personas,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_proveedor


class telefonos_personas (models.Model):
    numero_telefono=models.CharField(max_length=8)
    persona=models.ForeignKey(personas,on_delete=models.CASCADE)



class marcas(models.Model):
    descripcion_marca=models.CharField(max_length=20)
    categoria=models.CharField(max_length=1)
    def __str__(self):
        return self.descripcion_marca
    

class unidad_medidas(models.Model):
    descripcion_unidad_medida=models.CharField(max_length=20)
    def __str__(self):
        return self.descripcion_unidad_medida


class detalle_productos(models.Model):
    fecha_creacion=models.DateField(default=datetime.now)
    cantidad_min_stock=models.PositiveIntegerField()
    estado_producto=models.IntegerField(null=False,blank=False,choices=status,default=1)
    proveedor=models.ForeignKey(proveedores,on_delete=models.CASCADE)
    marca=models.ForeignKey(marcas,null=True,on_delete=models.CASCADE)
    unidad_medida=models.ForeignKey(unidad_medidas,on_delete=models.CASCADE)
    def toJSON(self): 
        item = model_to_dict(self)
        return item



class categoria_productos(models.Model):
    descripcion_categoria_productos=models.CharField(max_length=60)
    def __str__(self):
        return self.descripcion_categoria_productos


class regimens(models.Model):
    descripcion_regimen=models.CharField(max_length=30)
    impuesto_regimen=models.PositiveIntegerField()
    def __str__(self):
        return self.descripcion_regimen

class perfiles_colaboradores(models.Model):
    nombre_perfil=models.CharField(max_length=20)
    descripcion_perfil=models.CharField(max_length=40)
    def __str__(self):
        return self.nombre_perfil


class colaboradores(models.Model):
    DPI_Colaborador=models.CharField(max_length=16, unique=True)
    correo_colaborador=models.CharField(max_length=50)
    estado_colaborador=models.IntegerField(null=False,blank=False,choices=status,default=1)
    prefijo=models.CharField(max_length=4,default="COL")
    perfil_colaborador=models.ForeignKey(perfiles_colaboradores,on_delete=models.CASCADE)
    persona=models.ForeignKey(personas,on_delete=models.CASCADE)
    def __str__(self):
        return '%s %s' % (self.persona.nombre_persona, self.persona.apellido_persona)

class sucursales(models.Model):
    nombre_sucursal=models.CharField(max_length=40)
    direccion_sucursal=models.TextField()
    correo_sucursal=models.CharField(max_length=50)
    nit_sucursal=models.CharField(max_length=10, unique=True)
    telefono_sucursal=models.CharField(max_length=10)
    regimen=models.ForeignKey(regimens,on_delete=models.CASCADE)
    prefijo=models.CharField(max_length=4,default="SUC")
    colaborador_encargado=models.ForeignKey(colaboradores,on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre_sucursal

class productos(models.Model):
    existencia=models.PositiveIntegerField(default=0)
    nombre_producto=models.TextField()
    descripcion_producto=models.TextField(null=True,blank=True)
    categoria_producto=models.ForeignKey(categoria_productos,null=True,on_delete=models.CASCADE)
    precio_venta=models.DecimalField(max_digits=6,decimal_places=2)
    prefijo=models.CharField(max_length=4,default="PRO")
    detalle_producto=models.ForeignKey(detalle_productos,on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.productos.nombre_producto, self.productos.id)
      

    def toJSON(self):
        item = model_to_dict(self)
        item['detalle_producto'] = self.detalle_producto.toJSON()
        return item

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['id']
        

class agregar_productos(models.Model):
    fecha_registro=models.DateField(default=datetime.now)
    documento=models.CharField(max_length=30)
    nombre_producto=models.TextField()
    existencia=models.PositiveIntegerField ()
    sucursal=models.ForeignKey(sucursales,on_delete=models.CASCADE)
    cantidad_agregar=models.PositiveIntegerField()
    fecha_vencimiento=models.DateField(null=True,blank=True)
    precio_compra=models.DecimalField(max_digits=6,decimal_places=2)
    producto=models.ForeignKey( productos,on_delete=models.CASCADE)
    

class tipo_pagos(models.Model):
    descripcion_tipo_pago=models.CharField(max_length=30)
    def __str__(self):
        return self.descripcion_tipo_pago
    

class encabezado_factura(models.Model):
    cliente=models.ForeignKey(personas,on_delete=models.CASCADE)
    fecha_venta=models.DateField(default=datetime.now)
    sucursal=models.ForeignKey(sucursales,on_delete=models.CASCADE)
    colaborador=models.ForeignKey(colaboradores,on_delete=models.CASCADE)
    estado_factura=models.IntegerField(null=False,blank=False,choices=status,default=1)
    tipo_pago=models.ForeignKey(tipo_pagos,on_delete=models.CASCADE)
    descuento_total=models.DecimalField(default=0.00,max_digits=6,decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=6, decimal_places=2)

    def __str__(self):
        return self.cliente.nombre_persona

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['colaborador'] = self.colaborador.toJSON()
        item['sucursal'] = self.sucursal.toJSON()
        item['descuento_total'] = format(self.descuento_total, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha_venta'] = self.fecha_venta.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detalle_factura_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class detalle_factura(models.Model):
    venta=models.ForeignKey(encabezado_factura, on_delete=models.CASCADE)
    producto=models.ForeignKey(productos,on_delete=models.CASCADE)
    precio=models.DecimalField(   max_digits=9, decimal_places=4)
    cantidad=models.IntegerField(default=0)
    descuento=models.DecimalField(default=0.00,max_digits=9,decimal_places=2)
    subtotal=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    def __str__(self):
        return self.precio

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['producto'] = self.producto.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['cantidad'] = format(self.cantidad, '.2f')
        item['descuento'] = format(self.descuento, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')

        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

class clientes(models.Model):
    persona=models.ForeignKey(personas,on_delete=models.CASCADE)
    prefijo=models.CharField(max_length=4,default="CLI")


