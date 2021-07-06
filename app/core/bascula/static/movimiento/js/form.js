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
    
    //VEHICULO
    $('.btnAddVehiculo').on('click', function () {
        $('#modalVehiculo').modal('show');
    });

    $('#modalVehiculo').on('hidden.bs.modal', function (e) {
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
                $('#modalVehiculo').modal('hide');
            });
    });

    //CHOFER

    $('.btnAddChofer').on('click', function () {
        $('#modalChofer').modal('show');
    });

    $('#modalChofer').on('hidden.bs.modal', function (e) {
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
                $('#modalChofer').modal('hide');
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
            peso = peso == "" ? 0 : peso;
            if (action == 'add') {
                peso_entrada.val(parseInt(peso));
            } else {
                peso_salida.val(parseInt(peso));
            };

            if (peso == 0){
                message_error('Peso capturado no válido: [ ' + peso + ' ]' );
                return false;
            }
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

    ///////////////////////////
    //    EVENTO SUBMIT     
    ////////////////////////
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

});



// document.addEventListener('DOMContentLoaded', function (e) {
//     const form = document.getElementById('frmMovimiento');
//     const submitButton = form.querySelector('#btnGuardar');

//     fv = FormValidation.formValidation(form, {
//             locale: 'es_ES',
//             localization: FormValidation.locales.es_ES,
//             plugins: {
//                 trigger: new FormValidation.plugins.Trigger(),
//                 // submitButton: new FormValidation.plugins.SubmitButton(),
//                 submitButton: submitButton,
//                 // bootstrap: new FormValidation.plugins.Bootstrap(),
//                 icon: new FormValidation.plugins.Icon({
//                     valid: 'fa fa-check',
//                     invalid: 'fa fa-times',
//                     validating: 'fa fa-refresh',
//                 }),
//             },
//             fields: {
//                 nro_mic: {
//                     validators: {
//                         notEmpty: {},
//                         stringLength: {
//                             min: 2,
//                         },
//                         message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
//                         // regexp: {
//                         //     regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
//                         //     message: 'Debe ingresar sus dos nombres y solo utilizando caracteres alfabéticos'
//                         // },
//                     }
//                 },
//                 // last_name: {
//                 //     validators: {
//                 //         notEmpty: {},
//                 //         stringLength: {
//                 //             min: 2,
//                 //         },
//                 //         // regexp: {
//                 //         //     regexp: /^([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\'])+?$/i,
//                 //         //     message: 'Debe ingresar sus dos apellidos y solo utilizando caracteres alfabéticos'
//                 //         // },
//                 //     }
//                 // },
//                 // dni: {
//                 //     validators: {
//                 //         notEmpty: {},
//                 //         stringLength: {
//                 //             min: 10
//                 //         },
//                 //         digits: {},
//                 //         callback: {
//                 //             message: 'Introduce un número de cedula válido',
//                 //             callback: function (input) {
//                 //                 return validate_dni_ruc(input.value) || input.value === '9999999999';
//                 //             }
//                 //         },
//                 //         remote: {
//                 //             url: pathname,
//                 //             data: function () {
//                 //                 return {
//                 //                     obj: form.querySelector('[name="dni"]').value,
//                 //                     type: 'dni',
//                 //                     action: 'validate_data'
//                 //                 };
//                 //             },
//                 //             message: 'El número de cedula ya se encuentra registrado',
//                 //             method: 'POST'
//                 //         }
//                 //     }
//                 // },
//                 // mobile: {
//                 //     validators: {
//                 //         notEmpty: {},
//                 //         stringLength: {
//                 //             min: 7
//                 //         },
//                 //         digits: {},
//                 //         remote: {
//                 //             url: pathname,
//                 //             data: function () {
//                 //                 return {
//                 //                     obj: form.querySelector('[name="mobile"]').value,
//                 //                     type: 'mobile',
//                 //                     action: 'validate_data'
//                 //                 };
//                 //             },
//                 //             message: 'El número de teléfono ya se encuentra registrado',
//                 //             method: 'POST'
//                 //         }
//                 //     }
//                 // },
//                 // email: {
//                 //     validators: {
//                 //         notEmpty: {},
//                 //         stringLength: {
//                 //             min: 5
//                 //         },
//                 //         regexp: {
//                 //             regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
//                 //             message: 'El formato email no es correcto'
//                 //         },
//                 //         remote: {
//                 //             url: pathname,
//                 //             data: function () {
//                 //                 return {
//                 //                     obj: form.querySelector('[name="email"]').value,
//                 //                     type: 'email',
//                 //                     action: 'validate_data'
//                 //                 };
//                 //             },
//                 //             message: 'El email ya se encuentra registrado',
//                 //             method: 'POST'
//                 //         }
//                 //     }
//                 // },
//                 // address: {
//                 //     validators: {
//                 //         stringLength: {
//                 //             min: 4,
//                 //         }
//                 //     }
//                 // },
//                 // birthdate: {
//                 //     validators: {
//                 //         notEmpty: {
//                 //             message: 'La fecha es obligatoria'
//                 //         },
//                 //         date: {
//                 //             format: 'YYYY-MM-DD',
//                 //             message: 'La fecha no es válida'
//                 //         }
//                 //     },
//                 // },
//                 // image: {
//                 //     validators: {
//                 //         file: {
//                 //             extension: 'jpeg,jpg,png',
//                 //             type: 'image/jpeg,image/png',
//                 //             maxFiles: 1,
//                 //             message: 'Introduce una imagen válida'
//                 //         }
//                 //     }
//                 // },
//             },
//         }
//     )
//         .on('core.element.validated', function (e) {
//             if (e.valid) {
//                 const groupEle = FormValidation.utils.closest(e.element, '.form-group');
//                 if (groupEle) {
//                     FormValidation.utils.classSet(groupEle, {
//                         'has-success': false,
//                     });
//                 }
//                 FormValidation.utils.classSet(e.element, {
//                     'is-valid': false,
//                 });
//             }
//             const iconPlugin = fv.getPlugin('icon');
//             const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
//             iconElement && (iconElement.style.display = 'none');
//         })
//         .on('core.validator.validated', function (e) {
//             if (!e.result.valid) {
//                 const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
//                 messages.forEach((messageEle) => {
//                     const validator = messageEle.getAttribute('data-validator');
//                     messageEle.style.display = validator === e.validator ? 'block' : 'none';
//                 });
//             }
//         })
//         .on('core.form.valid', function () {
//             submit_formdata_with_ajax_form(fv);
//         });
// });