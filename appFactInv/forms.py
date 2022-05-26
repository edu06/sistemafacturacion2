
from django import forms
from appFactInv.models import categoria_productos, marcas, perfiles_colaboradores, personas,proveedores, regimens,telefonos_personas,detalle_productos,productos
from appFactInv.models import agregar_productos,clientes,colaboradores,sucursales,encabezado_factura, tipo_pagos, unidad_medidas,agregar_productos
from datetime import datetime


class formpersonas(forms.ModelForm):
    class Meta:
        model = personas
        fields= [
            'nombre_persona',
            'apellido_persona',
            'direccion_persona',
            'nit_persona',
            'telefono_persona',
        ]
        labels ={
            'nombre_persona'   :'Nombres Persona',
            'apellido_persona' :'Apellidos Persona',
            'direccion_persona':'Direccion Persona',
            'nit_persona'      :'Nit Persona',
            'telefono_persona' :'Telefono persona',
            }
        widgets ={
            'nombre_persona':forms.TextInput(attrs={'class':'form-control'}),
            'apellido_persona':forms.TextInput(attrs={'class':'form-control'}),
            'direccion_persona':forms.TextInput(attrs={'class':'form-control'}),
            'nit_persona':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_persona':forms.TextInput(attrs={'class':'form-control','placeholder':'Opcional'}),
            }


class formproveedores(forms.ModelForm):
    class Meta:
        model= proveedores
        fields= [
            'nombre_proveedor',
            'direccion_proveedor',
            'telefono_proveedor',
            'nit_proveedor',
            'estado_proveedor',
            'prefijo',
            ]

        labels ={
            'nombre_proveedor':'Nombre del Proveedor',
            'direccion_proveedor':'Dirección Proveedor',
            'telefono_proveedor':'Telefono Proveedor',
            'nit_proveedor':'Nit Proveedor',
            'estado_proveedor':'Estado',
            'prefijo':'Prefijo',
            }

        widgets ={
            'nombre_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'direccion_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'nit_proveedor':forms.TextInput(attrs={'class':'form-control'}),
            'estado_proveedor':forms.Select(attrs={'class':'form-control select2'}),
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            }

class formtelefonos_personas(forms.ModelForm):
    class Meta:
        model= telefonos_personas
        fields= [
            'numero_telefono',
            'persona'
            ]
        labels ={
            'numero_telefono':'Numero de Telefono',
            'persona':'Persona',
            }
        widgets ={
            'numero_telefono':forms.TextInput(attrs={'class':'form-control'}),
            'persona':forms.Select(attrs={'class':'form-control select2 '}),
            }

class formdetalle_producto(forms.ModelForm):
    class Meta:
        model = detalle_productos
        fields=[
            'fecha_creacion',
            'cantidad_min_stock',
            'estado_producto',
            'proveedor',
            'marca',
            'unidad_medida',
        ]

        labels = {    
            'fecha_creacion':'Fecha de Creacion',
            'cantidad_min_stock':'Cantidad Min Stock',
            'estado_producto':'Estado Producto',
            'numero_documento':'No Documento',
            'proveedor':'Proveedor',
            'marca':'Marca',
            'unidad_medida':'Unidad de Medida',
             }

        widgets = {
            
            'fecha_creacion':forms.DateInput(attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control datetimepicker-input','id':'fecha_venta','data-target':'#date_joined','data-toggle':'datetimepicke','readonly': True}),
            'cantidad_min_stock':forms.NumberInput(attrs={'class':'form-control'}),
            'estado_producto':forms.Select(attrs={'class':'form-control select2'}),
            'proveedor':forms.Select(attrs={'class':'form-control select2 ',}),
            'marca':forms.Select(attrs={'class':'form-control select2'}),
            'unidad_medida':forms.Select(attrs={'class':'form-control select2 '}),
            }

class formproducto(forms.ModelForm):
    class Meta:
        model = productos
        fields = [
            'existencia',
            'nombre_producto',
            'descripcion_producto',
            'categoria_producto',
            'prefijo',
            'precio_venta',
 
            
            ]
        labels = {
            'existencia':'Existencia',
            'nombre_producto': 'Nombre Producto',
            'categoria_producto':'Categoria Producto',
            'descripcion_producto': 'Descripcion Producto',
            'prefijo': 'Prefijo',
            'precio_venta':'Precio Venta',
      
            
            }
        widgets = {
            'existencia':forms.NumberInput(attrs={'class':'form-control','readonly':True}),
            'nombre_producto':forms.TextInput(attrs={'class':'form-control'}) ,
            'categoria_producto':forms.Select(attrs={'class':'form-control select2'}),
            'descripcion_producto':forms.TextInput(attrs={'class':'form-control','placeholder':'opcional'}) ,
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'precio_venta':forms.NumberInput(attrs={'class':'form-control'}),
       
            }

class formsucursales(forms.ModelForm):
    class Meta:
        model = sucursales
        fields=[
            'nombre_sucursal',
            'direccion_sucursal',
            'correo_sucursal',
            'nit_sucursal',
            'telefono_sucursal',
            'regimen',
            'prefijo',
            'colaborador_encargado',

        ]
        labels={
            'nombre_sucursal':'Nombre Sucursal',
            'direccion_sucursal':'Direccion Sucursal',
            'correo_sucursal':'Correo Electronico',
            'nit_sucursal':'Numero de Nit',
            'telefono_sucursal':'Telefono',
            'regimen':'Regimen',
            'prefijo': 'Prefijo',
            'colaborador_encargado':'Colaborador',
           }
        widgets = {
            'nombre_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'direccion_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'correo_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'nit_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'telefono_sucursal':forms.TextInput(attrs={'class':'form-control'}),
            'regimen':forms.Select(attrs={'class':'form-control select2'}),
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'colaborador_encargado':forms.Select(attrs={'class':'form-control select2'}),
            }

class formcolaboradores(forms.ModelForm):
    class Meta:
        model = colaboradores
        fields=[
         
            'DPI_Colaborador',
            'correo_colaborador',
            'estado_colaborador',
            'prefijo',
            'perfil_colaborador',
        ]
        labels={
            
            'DPI_Colaborador':'DPI Colaborador',
            'correo_colaborador':'Correo Electronico',
            'estado_colaborador': 'Estado',
            'prefijo':'Prefijo',
            'perfil_colaborador':'Perfil Colaborador',
        }
        widgets = {
            
            'DPI_Colaborador':forms.TextInput(attrs={'class':'form-control'}),
            'correo_colaborador':forms.TextInput(attrs={'class':'form-control'}),
            'estado_colaborador':forms.Select(attrs={'class':'form-control select2'}),
            'prefijo':forms.TextInput(attrs={'class':'form-control','readonly':True}),
            'perfil_colaborador':forms.Select(attrs={'class':'form-control select2'}),
            }

class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = encabezado_factura
        fields = '__all__'
        widgets = {
            'cliente':forms.Select(attrs={'class':'form-control select2','placeholder':'Buscar Clientes....'}),
            'fecha_venta':forms.DateInput(format='%Y-%m-%d',attrs={'readonly': True,'value':datetime.now().strftime('%Y-%m-%d'),'class': 'form-control','style': 'width: 40%'}),
            'sucursal':forms.Select(attrs={'class': 'form-control select2','style': 'width: 75%'}),
            'colaborador':forms.Select(attrs={'class': 'form-control select2','style': 'width: 75%'}),
            'estado_factura':forms.Select(attrs={'class':'form-control select2'}),
            'tipo_pago':forms.Select(attrs={'class':'form-control select2','style': 'width: 75%'}),
            'descuento_total':forms.TextInput(attrs={'readonly': True,'class': 'form-control','style': 'width: 40%'}),
             'total':forms.TextInput(attrs={'readonly': True,'class': 'form-control','style': 'width: 40%'})
        }

class formlogin(forms.ModelForm):
    class Meta:

        widgets ={
            'username':forms.TextInput(attrs={'class':'form-control','type':'text','placeholder':'Ingrese su usuario', 'name':'username'}),
            'password':forms.TextInput(attrs={'class':'form-control','type':'password','placeholder':'Ingrese su contraseña', 'name':'password'}),
            }


class formagregarproductos(forms.ModelForm):
    class Meta:
        model = agregar_productos
        fields = [
          
            'fecha_registro',
            'documento',
            'cantidad_agregar',
            'nombre_producto',
            'existencia',
            'fecha_vencimiento',
            'precio_compra',
            'sucursal'
            

            ]
        labels = {
            
            'fecha_registro':'Fecha ingreso',
            'documento': 'No Documento',
            'cantidad_agregar': 'Cantidad a agregar',
            'nombre_producto': 'Nombre producto',
            'existencia': 'Existencia actual',
            'sucursal':'Seleccione Sucursal',
            'fecha_vencimiento':'Fecha Vencimiento Producto',
            'precio_compra':'Precio compra Producto'

            }
        widgets = {

            'producto': forms.HiddenInput() ,
            'fecha_registro':forms.DateInput(attrs={'value':datetime.now().strftime('%Y-%m-%d'),'class':'form-control datetimepicker-input','id':'fecha_registro','data-target':'#date_joined','data-toggle':'datetimepicke','readonly': True}),
            'documento':forms.TextInput(attrs={'class':'form-control'}) ,
            'cantidad_agregar':forms.NumberInput(attrs={'class':'form-control'}),
            'nombre_producto':forms.TextInput(attrs={'class':'form-control','readonly': True}),
            'existencia':forms.NumberInput(attrs={'class':'form-control','readonly': True}),
            'sucursal':forms.Select(attrs={'class':'form-control select2'}),
            'fecha_vencimiento':forms.DateInput(attrs={'class':'form-control','placeholder':'Opcional'}),
            'precio_compra':forms.NumberInput(attrs={'class':'form-control'}),
            }

class formclientes(forms.ModelForm):
    class Meta:
        model= clientes
        fields= [
            'prefijo',
            ]
        labels ={
            'prefijo':'Prefijos',
            }
        widgets ={
            'prefijo':forms.TextInput( attrs={'class':'form-control','readonly':True}),
            }


class formcategoria_productos(forms.ModelForm):
    class Meta:
        model= categoria_productos
        fields= [
            'descripcion_categoria_productos',
            ]
        labels ={
            'descripcion_categoria_productos':'Ingrese Categoria Producto',
            
            }
        widgets ={
            'descripcion_categoria_productos':forms.TextInput(attrs={'class':'form-control'}),
            }

class formmarcas(forms.ModelForm):
    class Meta:
        model= marcas
        fields= [
            'descripcion_marca',
            'categoria',
            ]
        labels ={
            'descripcion_marca':'Ingrese la marca a registrar',
            'categoria':'Categoria marca (A) (B) o (C)',
            }
        widgets ={
            'descripcion_marca':forms.TextInput(attrs={'class':'form-control'}),
            'categoria':forms.TextInput(attrs={'class':'form-control'}),
            }

class formregimen(forms.ModelForm):
    class Meta:
        model= regimens
        fields= [
            'descripcion_regimen',
            'impuesto_regimen',
            ]
        labels ={
            'descripcion_regimen':'Ingrese el regimen de impuesto',
            'impuesto_regimen':    'Ingrese el porcentaje del regimen',
            }
        widgets ={
            'descripcion_regimen':forms.TextInput(attrs={'class':'form-control'}),
            'impuesto_regimen':forms.TextInput(attrs={'class':'form-control'}),
            }


class formunidadmedida(forms.ModelForm):
    class Meta:
        model= unidad_medidas
        fields= [
            'descripcion_unidad_medida',
            ]
        labels ={
            'descripcion_unidad_medida':'Ingrese una unidad de medida',
            
            }
        widgets ={
            'descripcion_unidad_medida':forms.TextInput(attrs={'class':'form-control'}),
            }


class formtipospago(forms.ModelForm):
    class Meta:
        model= tipo_pagos
        fields= [
            'descripcion_tipo_pago',
            ]
        labels ={
            'descripcion_tipo_pago':'Ingrese el tipo de pago',
            
            }
        widgets ={
            'descripcion_tipo_pago':forms.TextInput(attrs={'class':'form-control'}),
            }


class formperfilescolaboradores(forms.ModelForm):
    class Meta:
        model= perfiles_colaboradores
        fields= [
            'nombre_perfil',
            'descripcion_perfil',
            ]
        labels ={
            'nombre_perfil':'Ingrese el perfil del colaborador',
            'descripcion_perfil':'Ingrese la descripcion del perfil',
            
            }
        widgets ={
            'nombre_perfil':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion_perfil':forms.TextInput(attrs={'class':'form-control'}),
            }