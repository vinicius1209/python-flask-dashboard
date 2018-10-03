//Barra de pesquisa para pesquisar os componentes na table
$(document).ready(function(){

    $("#mySearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
       $("#myTasks tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

});

//Isso faz com que mesmo um segundo modal ser aberto, o anterior pode continuar o scroll
$(document).on('hidden.bs.modal', '.modal', function () {
	('.modal:visible').length && $(document.body).addClass('modal-open');
	
//tooltip
$('[data-toggle="tooltip"]').tooltip(); 
}); 