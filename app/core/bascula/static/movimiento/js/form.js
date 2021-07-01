$(function () {


    /* JAVASCRIPTS */
    
  

    //EVENTO SUBMIT     
    $('#frmMovimiento').on('submit', function (e) {
        e.preventDefault();
        $('select').prop('disabled',false);
        
        var parameters = new FormData(this);
        var action = $('input[name="action"]').val()
        var peso_entrada = $('input[name="peso_entrada"]').val()
        var peso_salida = $('input[name="peso_salida"]').val()
        if (action == 'add') {
            // alert(peso_entrada);
            if (peso_entrada <= 0) {
                message_error('Peso entrada es Cero');
                return false;
            }
        }
        else {
            // alert(peso_salida);
            if (peso_salida <= 0) {
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
    });
    

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
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

    $('.btnBascula').on('click', function (e) {
        e.preventDefault();
        var url = "/bascula/ajax_puerto_serial/" + this.value +"/";
        var parameters = {}
        submit_formdata_with_ajax('Notificación', '¿Capturar Peso de Bascula?',url,  parameters, function (data) {
            var action = $('#action').val();
            var result = data['resultado'];
            
            if (isNaN(result)){
                // alert(result);
                result = 0;
            }
            // alert(action);
            if (action == 'add'){
                $('#id_peso_entrada').val(parseInt(result));
            }else{
                $('#id_peso_salida').val(parseInt(result));
            };
                 
        

        });
    });



});