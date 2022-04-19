
import json
from xhtml2pdf import pisa
from django.db import  transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import context
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, UpdateView,
                                  View)
from django.contrib import messages
from appFactInv.forms import (SaleForm, formagregarproductos, formclientes,
                              formcolaboradores, formdetalle_producto, formmarcas, formperfilescolaboradores,
                              formpersonas, formproducto, formproveedores, formregimen,
                              formsucursales, formtelefonos_personas,formcategoria_productos, formmarcas, formtipospago, formunidadmedida)
from appFactInv.models import (agregar_productos, categoria_productos, clientes, colaboradores,
                               detalle_factura, detalle_productos,
                               encabezado_factura, marcas, perfiles_colaboradores, personas, productos,
                               proveedores, regimens, sucursales, telefonos_personas, tipo_pagos, unidad_medidas)


def Index(request):
    return render (request,"index.html")

def admin(request):
    return render(request,"admin.html")


#-------------------- AQUI INCIAN LOS METODOS PARA LAS BUSQUEDAS -----------------
def BuscarClientes(request):
    busqueda= request.GET.get("buscar")
    persona= clientes.objects.all()
    if busqueda:
        persona=clientes.objects.filter(
        Q(persona__nombre_persona__icontains=busqueda)|
        Q(persona__nit_persona__icontains=busqueda)
        ).distinct()
    return render (request,"BuscarClientes.html",{"persona":persona})


def BuscarFacturas(request):
    busqueda= request.GET.get("buscar")
    factura= encabezado_factura.objects.all().order_by('-id')
    if busqueda:
        factura=encabezado_factura.objects.filter(
        Q(cliente__nombre_persona__icontains=busqueda)|
        Q(cliente__nit_persona__icontains=busqueda)
        ).distinct()
    return render (request,"VerFacturas.html",{"factura":factura})

def BuscarProveedores(request):
    busqueda= request.GET.get("buscar")
    proveedor= proveedores.objects.all()
    if busqueda:
        proveedor=proveedores.objects.filter(
            Q(nombre_proveedor__icontains=busqueda)|
            Q(direccion_proveedor__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProveedores.html",{"proveedor":proveedor})


def BuscarColaboradores(request):
    busqueda= request.GET.get("buscar")
    colaborador= colaboradores.objects.all()

    if busqueda:
        colaborador=colaboradores.objects.filter(
            Q(nombre_persona__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarColaboradores.html",{"colaborador":colaborador})


def BuscarProductos(request):
    busqueda= request.GET.get("buscar")
    producto= productos.objects.all()

    if busqueda:
        producto=productos.objects.filter(
            Q(descripcion_producto__icontains=busqueda)|
            Q(nombre_producto__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarProductos.html",{"producto":producto})

def BuscarSucursales(request):
    busqueda= request.GET.get("buscar")
    sucursal= sucursales.objects.all()

    if busqueda:
        sucursal=sucursales.objects.filter(
            Q(nombre_sucursal__icontains=busqueda)
            ).distinct()
    return render (request,"BuscarSucursales.html",{"sucursal":sucursal})


def anular(request,pk):
    x=encabezado_factura.objects.filter(id=pk).update(estado_factura=False)
    return redirect('ver_facturas') 
  #  return render (request,"MensajeAnularFactura.html")
       


#-------------------------  AQUI INCIAN LAS CLASES CREATE  ----------------------------------#
 
class SaleCreateView(CreateView):
    model = encabezado_factura
    secondmodel=detalle_productos
    form_class = SaleForm
    template_name = 'Facturacion.html'
    success_url = reverse_lazy('crear_facturas')
    url_redirect = success_url

    @method_decorator(csrf_exempt) # esto sirve para deshabilitar la trasferencia del post 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        data = {} # la data la convertimos en un diccionario 
        try:
            action = request.POST['action'] # a la variable action le asignamos la acccion que se hara 
            if action == 'search_products': # si action es igual a el nombre de la acccion del html 
                data = []    
                prods = productos.objects.filter(nombre_producto__icontains=request.POST['term'])[0:10]
                
                for i in prods:  # recorrremos la variable prods con un for  
                    item = i.toJSON() # y lo recorrido lo vamos almacenando en la variable item transfomado a formato JSON ya que desde el modelo pasamos a JSON la informacion 
                    item['value'] = i.nombre_producto
                    data.append(item)
           
            elif action == 'add':
                with transaction.atomic():  # si llegara a pasar un error en la ejecucion siguiente no se guardara nada. 
                    vents = json.loads(request.POST['vents']) #recuperamos lo que nos devuelve POST por medio de la funcion de javascript  
                    print(vents)
                    sale = encabezado_factura()
                    sale.fecha_venta = vents['fecha_venta']
                    sale.cliente_id = vents['cliente']
                    sale.colaborador_id=vents['colaborador']
                    sale.sucursal_id=vents['sucursal']
                    sale.tipo_pago_id=vents['tipo_pago']
                    sale.descuento_total=float(vents['descuento_total'])
                    sale.total = float(vents['total'])
                    sale.save()
                    
                    for i in vents['products']:
                        det = detalle_factura()     
                        det.venta_id=sale.id  
                        det.producto_id=i['id']
                        det.cantidad=int(i['cant_facturar'])
                        det.descuento=float(i['desc_producto'])
                        det.subtotal=float(i['varsubtotal'])  
                        det.precio=float(i['precio_venta'])                 
                        det.save()    
                       
                        
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class CrearSucursales(CreateView):
    model = sucursales
    template_name='CrearSucursales.html'
    form_class = formsucursales
    success_url='/crear_sucursales'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearSucursales, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            guardarsucursal = form.save(commit=False)
            guardarsucursal.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))


class CrearProveedores(CreateView):
    model = proveedores
    template_name='CrearProveedores.html'
    form_class = formproveedores
    second_form_class = formpersonas
    success_url='/crear_proveedores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearProveedores, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarproveedor = form.save(commit=False)
            guardarproveedor.persona_contacto = form2.save()
            guardarproveedor.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class CrearColaboradores(CreateView):
    model = colaboradores
    template_name='CrearColaboradores.html'
    form_class = formcolaboradores
    second_form_class = formpersonas
    success_url='/crear_colaboradores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex =super(CrearColaboradores, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarcolab = form.save(commit=False)
            guardarcolab.persona = form2.save()
            guardarcolab.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))

class CrearTelefonosPersonas(CreateView):
    model = telefonos_personas
    template_name='CrearTelefonosPersonas.html'
    form_class = formtelefonos_personas
    success_url='/agregar_telefonos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearTelefonosPersonas, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)
        return contex  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            guardartelefono = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))

class CrearProductos(CreateView):
    model = productos
    template_name='CrearProductos.html'
    form_class = formproducto
    second_form_class = formdetalle_producto
    success_url='/crear_productos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearProductos, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarproducto = form.save(commit=False)
            guardarproducto.detalle_producto = form2.save()
            guardarproducto.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))


class CrearClientes(CreateView):
    model = clientes
    template_name='CrearClientes.html'
    form_class = formclientes
    second_form_class = formpersonas
    success_url='/crear_clientes'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        contex = super(CrearClientes, self).get_context_data(**kwargs)
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)  # AQUI AGREGAMOS NUESTRO PRIMER FORM A NUESTRO CONTEXTO
        if 'form2' not in contex:
            contex['form2'] = self.second_form_class(self.request.GET)
        return contex  # hasta aqui agregamos los dos forms al contexto

    # para guardar la informacion de los dos formularios y que se cree la relacion sobrescribimos el metodo POST
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            guardarcliente = form.save(commit=False)
            guardarcliente.persona = form2.save()
            guardarcliente.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form,form2=form2))

class Crearmarca(CreateView):
    model = marcas
    template_name='crear_marcas.html'
    form_class = formmarcas
    success_url='/crear_marcas'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object    

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):    
        contex = super(Crearmarca,self).get_context_data(**kwargs)
        contex ['lmarcas']= self.get_queryset()
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)            
        return  contex
               
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))
        

class CrearCategoriaProducto(CreateView):
    model = categoria_productos
    template_name='crear_categoria_productos.html'
    form_class = formcategoria_productos
    success_url='/crear_categoria_productos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object    

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):    
        contex = super(CrearCategoriaProducto,self).get_context_data(**kwargs)
        contex ['lcategoria']= self.get_queryset()
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)            
        return  contex
               
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))

   
class CrearRegimen(CreateView):
    model = regimens
    template_name='crear_regimen.html'
    form_class = formregimen
    success_url='/crear_regimen'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object    
        
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):    
        contex = super(CrearRegimen,self).get_context_data(**kwargs)
        contex ['lregimen']= self.get_queryset()
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)            
        return  contex
               
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))


class CrearUnidadMedida(CreateView):
    model = unidad_medidas
    template_name='crear_unidad_medidas.html'
    form_class = formunidadmedida
    success_url='/crear_unidad_medidas'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object    
        
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):    
        contex = super(CrearUnidadMedida,self).get_context_data(**kwargs)
        contex ['lunidadmedida']= self.get_queryset()
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)            
        return  contex
               
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))
    

class CrearTipoPago(CreateView):
    model = tipo_pagos
    template_name='crear_tipo_pagos.html'
    form_class = formtipospago
    success_url='/crear_tipo_pagos'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object    
        
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):    
        contex = super(CrearTipoPago,self).get_context_data(**kwargs)
        contex ['lpagos']= self.get_queryset()
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)            
        return  contex
               
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))
    

class CrearPerfilColaboradores(CreateView):
    model = perfiles_colaboradores
    template_name='crear_perfil_colaboradores.html'
    form_class = formperfilescolaboradores
    success_url='/crear_perfil_colaboradores'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object    
        
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):    
        contex = super(CrearPerfilColaboradores,self).get_context_data(**kwargs)
        contex ['lperfiles']= self.get_queryset()
        if 'form' not in contex:
            contex['form'] = self.form_class(self.request.GET)            
        return  contex
               
    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'!Registro Guardado Exitosamente!')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))
    



#----------------------- AQUI INCIAN LAS CLASES DE EDITAR ----------------------------------------------------------#

class EditarMarcas(UpdateView):
    model=marcas
    form_class=formmarcas
    template_name='crear_marcas.html'
    success_url='/crear_marcas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lmarcas'] = marcas.objects.filter()
        return context


class EditarCategoriaProducto(UpdateView):
    model=categoria_productos
    form_class=formcategoria_productos
    template_name='crear_categoria_productos.html'
    success_url='/crear_categoria_productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lcategoria'] = categoria_productos.objects.filter()
        return context


class EditarRegimen(UpdateView):
    model=regimens
    form_class=formregimen
    template_name='crear_regimen.html'
    success_url='/crear_regimen'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lregimen'] = regimens.objects.filter()
        return context

class EditarUnidadMedida(UpdateView):
    model=unidad_medidas
    form_class=formunidadmedida
    template_name='crear_unidad_medidas.html'
    success_url='/crear_unidad_medidas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lunidadmedida'] = unidad_medidas.objects.filter()
        return context

class EditarPerfilColaboradores(UpdateView):
    model=perfiles_colaboradores
    form_class=formperfilescolaboradores
    template_name='crear_perfil_colaboradores.html'
    success_url='/crear_perfil_colaboradores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lperfiles'] = perfiles_colaboradores.objects.filter()
        return context

class EditarTipoPagos(UpdateView):
    model=tipo_pagos
    form_class=formtipospago
    template_name='crear_tipo_pagos.html'
    success_url='/crear_tipo_pagos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lpagos'] = tipo_pagos.objects.filter()
        return context

class EditarProductos(UpdateView):
    model=productos
    second_model=detalle_productos
    template_name='EditarProductos.html'
    form_class = formproducto
    second_form_class= formdetalle_producto
    success_url='/buscar_productos'

    def get_context_data(self,**kwargs):
        context= super(EditarProductos,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        productos=self.model.objects.get(id=pk)
        detalle_productos=self.second_model.objects.get(id=productos.detalle_producto_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=detalle_productos)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_producto = kwargs['pk']
        productos = self.model.objects.get(id=id_producto)
        detalle_productos = self.second_model.objects.get(id=productos.detalle_producto_id)


        form = self.form_class(request.POST, instance=productos)
        form2 = self.second_form_class(request.POST,instance=detalle_productos)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

class EditarSucursales(UpdateView):
    model=sucursales
    template_name='EditarSucursales.html'
    form_class = formsucursales
    success_url='/buscar_sucursales'

    def get_context_data(self,**kwargs):
        context= super(EditarSucursales,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
  
        if 'form' not in context:
            context ['form']=self.form_class()

        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_sucursal = kwargs['pk']
        sucursales= self.model.objects.get(id=id_sucursal)
     
        form = self.form_class(request.POST, instance=sucursales)
        if form.is_valid():
            form.save()
        
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class EditarProveedores(UpdateView):
    model=proveedores
    second_model=personas
    template_name='EditarProveedores.html'
    form_class = formproveedores
    second_form_class= formpersonas
    success_url='/buscar_proveedores'

    def get_context_data(self,**kwargs):
        context= super(EditarProveedores,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        proveedores=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=proveedores.persona_contacto_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_proveedor = kwargs['pk']
        proveedores = self.model.objects.get(id=id_proveedor)
        personas = self.second_model.objects.get(id=proveedores.persona_contacto_id)
        form = self.form_class(request.POST, instance=proveedores)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class EditarClientes(UpdateView):
    model=clientes
    second_model=personas
    template_name='EditarClientes.html'
    form_class = formclientes
    second_form_class= formpersonas
    success_url='/buscar_clientes'

    def get_context_data(self,**kwargs):
        context= super(EditarClientes,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        clientes=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=clientes.persona_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_cliente = kwargs['pk']
        clientes = self.model.objects.get(id=id_cliente)
        personas = self.second_model.objects.get(id=clientes.persona_id)
        form = self.form_class(request.POST, instance=clientes)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class EditarColaboradores(UpdateView):
    model=colaboradores
    second_model=personas
    template_name='EditarColaboradores.html'
    form_class = formcolaboradores
    second_form_class= formpersonas
    success_url='/buscar_colaboradores'

    def get_context_data(self,**kwargs):
        context= super(EditarColaboradores,self).get_context_data(**kwargs)
        pk=self.kwargs.get('pk',0)
        colaboradores=self.model.objects.get(id=pk)
        personas=self.second_model.objects.get(id=colaboradores.persona_id)
        if 'form' not in context:
            context ['form']=self.form_class()
        if 'form2' not in context:
            context['form2']=self.second_form_class(instance=personas)
        context['id']=pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_colaborador = kwargs['pk']
        colaboradores = self.model.objects.get(id=id_colaborador)
        personas = self.second_model.objects.get(id=colaboradores.persona_id)
       
        form = self.form_class(request.POST, instance=colaboradores)
        form2 = self.second_form_class(request.POST, instance=personas)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

#---------------------------  AQUI INICIAN LAS CLASES  AGREGAR  ----------------------------------------------#

class AgregarProductos(UpdateView):
    model=productos
    secondmodel=agregar_productos
    template_name='AgregarProductos.html'
    form_class = formagregarproductos
    success_url='/buscar_productos'

    def post(self, request, *args, **kwargs):
        self.object=self.get_object
        form = self.form_class(request.POST)  
        dato= productos.objects.get(pk = self.kwargs.get('pk')) #aqui traigo la pk de la url
        form.instance.producto=dato # aqui lo asigno al campo producto del form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data( form=form))

#---------------------------------  AQUI INCIAN LAS CLASES VARIAS  -------------------------------------#

class PDFFactura(View):   #CLASE PARA LA GENERACION DE TICKET EN PDF
    def get(self,request,*args,**kwargs):
        try:
            template= get_template('pdffact.html')
            context = {
                'venta':encabezado_factura.objects.get(pk=self.kwargs['pk'])

            }
            html = template.render(context)
            response =HttpResponse(content_type='application/pdf')
            pisaStatus=pisa.CreatePDF(html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Index'))








