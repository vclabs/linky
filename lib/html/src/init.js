$(document).ready(function() {
    var table = $('#datatable').DataTable();
     
    $('#datatable tbody').on('click', 'tr', function () {
        var data = table.row( this ).data();
        alert( 'You clicked on '+data[0]+'\'s row' );
    } );
} );