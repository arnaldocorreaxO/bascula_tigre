$(function () {
    var action = $('input[name="action"]').val();
    var peso_entrada = $('input[name="peso_entrada"]');
    var peso_salida = $('input[name="peso_salida"]');

    /*HABILITA EDICION DE PESO PARA VILLETA INTERNO */
    var select_cliente = $('select[name="cliente"]');
    select_cliente.change(function () {
        if (action == 'add') {
            if (select_cliente.val() == 1) {
                peso_entrada.prop('readonly', false);
            } else {
                peso_entrada.val(0);
                peso_entrada.prop('readonly', true);
            }
        }
    });

    //EVENTO SUBMIT     
    $('#frmMovimiento').on('submit', function (e) {
        e.preventDefault();
        $('select').prop('disabled',false);               
        
        var parameters = new FormData(this);        
        
        if (action == 'add') {            
            if (peso_entrada.val() <= 0) {
                message_error('Peso entrada es Cero');
                return false;
            }
        }
        else {
            // alert(peso_salida);
            if (peso_salida.val() <= 0) {
                message_error('Peso Salida es Cero');
                return false;
            }

        };      
        
        parameters.append('action', action);
        submit_formdata_with_ajax('Notificación',
            '¿Estas seguro de realizar la siguiente acción?',
            window.location.pathname,
            parameters,
            function (request) {                 
                if (action != 'add') {
                    dialog_action('Notificación', '¿Desea Imprimir el Comprobante?', function () {
                        window.open('/bascula/movimiento/print/' + request.id + '/', '_blank');
                        location.href = '/bascula/movimiento';
                    }, function () {
                        location.href = '/bascula/movimiento';
                    });                    
                } else {
                    location.href = '/bascula/movimiento';
                }
            });
            if (action != 'add') {
                $('select').prop('disabled',true); 
            }
                          
    });
    
    //VEHICULO
    $('.btnAddVehiculo').on('click', function () {
        $('#myModalVehiculo').modal('show');
    });

    $('#myModalVehiculo').on('hidden.bs.modal', function (e) {
        $('#frmVehiculo').trigger('reset');
    })

    //SUBMIT VEHICULO
    $('#frmVehiculo').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create-vehiculo');
        submit_formdata_with_ajax('Notificación',
            '¿Estas seguro de crear al siguiente Vehiculo?',window.location.pathname,  parameters, function (response) {
                // console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="vehiculo"]').append(newOption).trigger('change');
                $('#myModalVehiculo').modal('hide');
            });
    });

    //CHOFER

    $('.btnAddChofer').on('click', function () {
        $('#myModalChofer').modal('show');
    });

    $('#myModalChofer').on('hidden.bs.modal', function (e) {
        $('#frmChofer').trigger('reset');
    })

    //SUBMIT Chofer
    $('#frmChofer').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create-chofer');
        submit_formdata_with_ajax( 'Notificación',
            '¿Estas seguro de crear al siguiente Chofer?',window.location.pathname,  parameters, function (response) {
                // console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="chofer"]').append(newOption).trigger('change');
                $('#myModalChofer').modal('hide');
            });
    });

    //////////////////////////////
    // CAPTURAR PESO DE BASCULA
    //////////////////////////////
    $('.btnBascula').on('click', function (e) {
        e.preventDefault();
        var url = "/bascula/ajax_puerto_serial/" + this.value + "/";
        var parameters = {}
        submit_formdata_with_ajax('Notificación', '¿Capturar Peso de Bascula?', url, parameters, function (data) {
            var peso = data['peso'];
            if (isNaN(peso)) {
                peso = 0;
            }; 
            console.log(action);
            if (action == 'add') {
                peso_entrada.val(parseInt(peso));
            } else {
                peso_salida.val(parseInt(peso));
            };
        });
    });


    // IMPLEMENTACION DE SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });


    // HABILITA BOTON SAVE
    setInterval(validarCampos, 500);

    function validarCampos() {
        if (action == 'add') {
            if (peso_entrada.val() == 0){ //si el input es cero
                $('#btnGuardar').attr('disabled', 'disabled');
            }
            else { // si tiene un valor diferente a cero
                $('#btnGuardar').removeAttr("disabled");
            }
        }
        else {
            if (peso_salida.val()==0){ //si el input es cero
                $('#btnGuardar').attr('disabled', 'disabled');
            }
            else { // si tiene un valor diferente a cero
                $('#btnGuardar').removeAttr("disabled");
            }
        }
    }

    

});