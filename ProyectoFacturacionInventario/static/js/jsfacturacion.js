var tblProducts;
var vents = {  
    items: {   // items contiene un diccionario con todo lo que tiene cabecera y detalle 
        fecha_venta: '',
        cliente: '' ,
        sucursal:'',
        colaborador:'',
        tipo_pago:'',
        descuento_total:'0.00',
        total: '00.00',
        products:[]  
    },
    calcular_factura: function () {
        
        //variable cont va ir suamando todos los valores de la variable local varsubtotal
        var cont = 0.00;
        // variable contador para ir sumando el descuento que se hace en el datatable 
        var cont2 = 0.00;
        //con each hago referencia con this a items y a lo que tiene products. y me muevo con pos con mi diccionario dict 
        $.each(this.items.products, function (pos, dict) { 
                  
        //aqui se va sumando a contador2 los valores que esta en la variable desc_producto
        
        
         
        //entonces digo que la variable local de subtotal, es igual a la variable local cant facturar * por la variable que viene en productos precio de venta 
        dict.varsubtotal =  dict.cant_facturar * parseFloat(dict.precio_venta)- parseFloat(dict.desc_producto);
        
        //aqui se va agregando la suma de todos los subtotales que tiene la variable varsubtotal a la variable contador 
        cont+=dict.varsubtotal;
        cont2+=dict.desc_producto;    
    
    });
  
         // Aqui se asigna el valor de contador2 a la variable de products.
         this.items.descuento_total= cont2;
  
  
        // Entonces el valor que tengo en la variable contador lo debo de agregar a la variable correspondiente que traigo de products  
         this.items.total= cont;

  
       //aqui se muestra en el input de descuento el valor del descuento
        $('input[name="descuento_total"]').val(this.items.descuento_total.toFixed(2));


          // y muestro lo que tengo en la variable de products en un input que se llama total. 
        $('input[name="total"]').val(this.items.total.toFixed(2));

        },
    
    
    add: function (item) {   // esta funcion add se utiliza para insertar un registro en el datatable 
        this.items.products.push(item);
        this.list();     // para llamar el metodo list que lista los productos en el datatable 
       },

        
    
    list: function () {   // funcion que lista los registros ya agregados al Datatable
    this.calcular_factura();  // pero primero llama a la funcion que realiza los calculos antes de presentar o listar la informacion. 

    tblProducts =$('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            columns: [
                {"data": "id"},
                {"data": "existencia"},
                {"data": "cant_facturar"},  // estos son items que yo no tengo en mi modelo detalle_factura y lo defino aqui para enviarselo al modelo 
                {"data": "nombre_producto"},
                {"data": "precio_venta"},
                {"data": "desc_producto"},   // estos son items que yo no tengo en mi modelo detalle_factura y lo defino aqui para enviarselo al modelo 
                {"data": "varsubtotal"},    // estos son items que yo no tengo en mi modelo detalle_factura y lo defino aqui para enviarselo al modelo
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-info btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
               
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant_facturar" class="form-control form-control-sm" autocomplete="off" value="' + row.cant_facturar + '">';
                    }
                },
                
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Q ' + parseFloat(data).toFixed(2);
                }
            },
                {
                    targets: [5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="number" name="desc_producto" class="form-control form-control-sm" autocomplete="off" value="' + row.desc_producto + '">';
                    }
                },
                
                
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return 'Q ' + parseFloat(data).toFixed(2);
                    }
                },

            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="cant_facturar"]');

            },


            initComplete: function (settings, json) {

            }
        });
 
    },
};

$(function () {   //Funcion para buscar los productos y traerlos en formato json al html  utilizando autocomplete de las librerias JQuery ui 

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 300,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();  //detiene el evento para poder seguir haciendo busquedas 
      
            /* se definen estas variables  para enviarlas al modelo ya que no las trae el array de products */
            ui.item.cant_facturar = 1;   
            ui.item.desc_producto = 0.00;
            ui.item.varsubtotal = 0.00;
            console.log(vents.items);
            vents.add(ui.item); // llama a la funcion add que realiza el push o insert de los objetos en el datatable 
            $(this).val('');
        }
    });


  
  
  
    // evento cantidad
  $('#tblProducts tbody')
  .on('click','a[rel="remove"]',function(){
    var tr = tblProducts.cell($(this).closest('td, li')).index();
    vents.items.products.splice(tr.row,1);
    vents.list();

  })
  .on('change','input[name="cant_facturar"]', function () {
    console.clear();
    var cant = parseInt($(this).val());
    var tr = tblProducts.cell($(this).closest('td, li')).index();
    vents.items.products[tr.row].cant_facturar=cant;
    vents.calcular_factura();
    $('td:eq(6)', tblProducts.row(tr.row).node()).html('Q' + vents.items.products[tr.row].varsubtotal.toFixed(2));
});

//evento descuento
$('#tblProducts tbody') // llamamos a tabla de productos 
.on('click','a[rel="remove"]',function(){
  var tr = tblProducts.cell($(this).closest('td, li')).index();
  vents.items.products.splice(tr.row,1);
  vents.list();
})
.on('change','input[name="desc_producto"]', function () {  // activamos el evento change o  cambio en el imput llamado desc_producto que hemos definido 
  console.clear();
  var desc = parseFloat($(this).val());
  
  var tr = tblProducts.cell($(this).closest('td, li')).index();
  vents.items.products[tr.row].desc_producto=desc;
  vents.calcular_factura();
  $('td:eq(6)', tblProducts.row(tr.row).node()).html('Q' + vents.items.products[tr.row].varsubtotal.toFixed(2));
});



//Evento para enviar la factura submit

$('form').on('submit',function (e) {
    e.preventDefault(); //detiene el evento del  submit para poder enviar los datos mediante ajax 

    if(vents.items.products.length === 0){  //validacion para que no deje guardar si no tienen items agregado. 
        message_error('Debe al menos tener un item en su detalle de venta');
        return false;
    }

    
 // los parametros que se envian pero que se tienen que ingresar manualmente. 
    
    vents.items.fecha_venta = $('input[name="fecha_venta"]').val(); //mandamos la fecha que lo ingresa el sistema en este caso. 
    vents.items.cliente = $('select[name="cliente"]').val(); //mandamos el id del cliente seleccionado 
    vents.items.sucursal = $('select[name="sucursal"]').val(); //mandamos el id de la sucursal
    vents.items.colaborador = $('select[name="colaborador"]').val(); //mandamos el id de  colaborador 
    vents.items.tipo_pago = $('select[name="tipo_pago"]').val();
    vents.items.descuento_total = $('input[name="descuento_total"]').val();
    vents.items.total = $('input[name="total"]').val();
    
    var parameters = new FormData(); //este formData se alimentaba del formulario pero ahora se hara manualmente con los parametros de abajo. 
    parameters.append('action', $('input[name="action"]').val());  //colocamos el action en el parametro porque lo recuperamos de nuestro imput llamado action  
    parameters.append('vents', JSON.stringify(vents.items));  // convierte diccionario a tipo string y manda empaquetado como parametro los valores de vents
    
    
    submit_with_ajax(window.location.pathname,'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
     location.href = '/crear_facturas';  // al realizar la acccion de guardado retorna a la misma pantalla/ 
        });


});

vents.list();

function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
    theme: 'material',
    title: title,
    icon: 'fa fa-info',
    content: content,
    columnClass: 'small',
    typeAnimated: true,
    cancelButtonClass: 'btn-primary',
    draggable: true,
    dragWindowBorder: false,
    buttons: {
        info: {
            text: "Si",
            btnClass: 'btn-primary',
            action: function () {
                $.ajax({
                    url: url, //window.location.pathname
                    type: 'POST',
                    data: parameters,
                    dataType: 'json',
                    processData: false,
                    contentType: false,
                }).done(function (data) {

                    console.log(data);

                    if (!data.hasOwnProperty('error')) {
                        callback();
                        return false;
                    }

                }).fail(function (jqXHR, textStatus, errorThrown) {
                    alert(textStatus + ': ' + errorThrown);
                }).always(function (data) {

                });
            }
        },
        danger: {
            text: "No",
            btnClass: 'btn-red',
            action: function () {

            }
        },
    }
});
}

});

