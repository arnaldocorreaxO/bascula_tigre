var tblData;
var input_daterange;
var columns = [];

// function initTable() {
    
//     tblData = $('#data').DataTable({
//         responsive: true,
//         autoWidth: false,
//         destroy: true,
//         // deferRender: true,
//         // processing: true,
//         // serverSide: true,
//     });

//     $.each(tblData.settings()[0].aoColumns, function (key, value) {
//         columns.push(value.sWidthOrig);
//     });

//     $('#data tbody tr').each(function (idx) {
//         $(this).children("td:eq(0)").html(idx + 1);
//         console.log(idx+1);
//     });
// };

function getData(all) {
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,  
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
           
            },
            //Sin este da error de length
            dataSrc: ""
        },
        order: [[4, 'desc']],
        paging: true,
        ordering: true,
        searching: true,  
        columns: [
            {data: "id"},
            {data: "nro_ticket"},
            {data: "fecha"},
            {data: "vehiculo"},
            {data: "chofer"},
            {data: "producto"},
            {data: "peso_entrada"},
            {data: "peso_salida"},
            {data: "peso_neto"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/bascula/movimiento/update/' + row.id + '/" class="btn btn-warning btn-flat" data-toggle="tooltip" title="Salida Báscula">SALIDA<i class="fas fa-truck"></i></a> ';
                    buttons += '<a href="/bascula/movimiento/print/' + row.id + '/" target="_blank" class="btn btn-dark btn-flat" data-toggle="tooltip" title="Imprimir Ticket Báscula"><i class="fas fa-print"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}


$(function () {  
    getData(true);
});
