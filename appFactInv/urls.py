from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required 
from appFactInv.views import CrearTipoPago, Index,CrearProveedores,EditarProveedores,BuscarProveedores,CrearClientes,CrearTelefonosPersonas,CrearProductos,EditarProductos,BuscarFacturas
from appFactInv.views import BuscarProductos,BuscarProductosDelete,CrearColaboradores,BuscarColaboradores,EditarColaboradores,CrearSucursales,AgregarProductos,EditarTipoPagos
from appFactInv.views import BuscarSucursales,EditarSucursales,SaleCreateView,BuscarProductosAgregar,EditarRegimen,EditarUnidadMedida,EditarPerfilColaboradores
from appFactInv.views import BuscarClientes,EditarClientes,PDFFactura,admin,Crearmarca,CrearRegimen,CrearUnidadMedida,CrearPerfilColaboradores,EditarMarcas,CrearCategoriaProducto,EditarCategoriaProducto
from usuarios.views import Login,logoutusuario

urlpatterns=[ 
    
    path('index/',login_required(Index),name='index'),
    
    path('crear_proveedores/',login_required(CrearProveedores.as_view()),name="crear_proveedores"),
    path('crear_clientes/',login_required(CrearClientes.as_view()),name="crear_clientes"),
    path('crear_productos/',login_required(CrearProductos.as_view()),name="crear_productos"),
    path('crear_colaboradores/',login_required(CrearColaboradores.as_view()),name="crear_colaboradores"),
    path('crear_sucursales/',login_required(CrearSucursales.as_view()),name="crear_sucursales"),
    path('crear_facturas/',login_required(SaleCreateView.as_view()),name="crear_facturas"),



    path('crear_marcas/',login_required(Crearmarca.as_view()),name="crear_marcas"),
    path('editar_marca/<int:pk>/',login_required(EditarMarcas.as_view()),name="editar_marca"),

    path('crear_categoria_productos/',login_required(CrearCategoriaProducto.as_view()),name="crear_categoria_productos"),
    path('editar_categoria_productos/<int:pk>/',login_required(EditarCategoriaProducto.as_view()),name="editar_categoria_productos"),


    path('editar_tipo_pagos/<int:pk>/',login_required(EditarTipoPagos.as_view()),name="editar_tipo_pagos"), 
    path('editar_regimen/<int:pk>/',login_required(EditarRegimen.as_view()),name="editar_regimen"), 
    path('crear_regimen/',login_required(CrearRegimen.as_view()),name="crear_regimen"),
   
    path('crear_unidad_medidas/',login_required(CrearUnidadMedida.as_view()),name="crear_unidad_medidas"),
    path('editar_unidad_medida/<int:pk>/',login_required(EditarUnidadMedida.as_view()),name="editar_unidad_medida"), 
   
    path('crear_tipo_pagos/',login_required(CrearTipoPago.as_view()),name="crear_tipo_pagos"),
    path('crear_perfil_colaboradores/',login_required(CrearPerfilColaboradores.as_view()),name="crear_perfil_colaboradores"),
    path('editar_perfil_colaboradores/<int:pk>/',login_required(EditarPerfilColaboradores.as_view()),name="editar_perfil_colaboradores"),
    path('crear_pdf/<int:pk>',login_required(PDFFactura.as_view()),name="crear_pdf"),
    
    path('editar_clientes/<int:pk>',login_required(EditarClientes.as_view()), name="editar_clientes"),
    path('editar_proveedores/<int:pk>',login_required(EditarProveedores.as_view()), name="editar_proveedores"),
    path('editar_productos/<int:pk>',login_required(EditarProductos.as_view()), name="editar_productos"),
    path('editar_colaboradores/<int:pk>',login_required(EditarColaboradores.as_view()),name="editar_colaboradores"),
    path('editar_sucursales/<int:pk>',login_required(EditarSucursales.as_view()), name="editar_sucursales"),

    
    path('buscar_proveedores/',login_required(BuscarProveedores),name="buscar_proveedores"),
    path('buscar_clientes/',login_required(BuscarClientes),name="buscar_clientes"),
    path('buscar_productos/',login_required(BuscarProductos),name="buscar_productos"),
    path('buscar_productos_delete/',login_required (BuscarProductosDelete),name="buscar_productos_delete"),
    path('buscar_productos_agregar/',login_required (BuscarProductosAgregar),name="buscar_productos_agregar"),
    path('buscar_colaboradores/',login_required(BuscarColaboradores),name="buscar_colaboradores"),
    path('buscar_sucursales/',login_required(BuscarSucursales),name="buscar_sucursales"),
    path('buscar_facturas/',login_required(BuscarFacturas),name="buscar_facturas"),
    path('agregar_telefonos/',login_required(CrearTelefonosPersonas.as_view()),name="agregar_telefonos"),
    path('agregar_productos/<int:pk>',login_required(AgregarProductos.as_view()),name="agregar_productos"),

       
    path('admin/',admin,name="admin"),

    #----------- URLS PARA LOGIN Y LOGOUT -----------------------#
    path('',Login.as_view(), name='login'),
    path('logout/',login_required(logoutusuario), name='logout'),
   
    ]
