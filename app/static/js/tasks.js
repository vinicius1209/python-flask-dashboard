/************************ DOCUMENT *************************************/
//Barra de pesquisa para pesquisar os componentes na table
$(document).ready(function(){

    $("#mySearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
       $("#myTasks tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

});

/*************************** UTILS *******************************/

//Tooltip para cada linha da tabela
$('[data-toggle="tooltip"]').tooltip();

//Obrigado Leonardo
$('.modal').on('shown.bs.modal', function () {
  $(this).find("#id").trigger('focus')
})

/************************** CONTEXT MENU ******************************/

$.contextMenu({
    selector: '.context-menu',
    items: {
        forum: {
            name: "Fórum",
			icon: "edit",
            callback: function(key, opt){
                
            }
        },
		log: {
			name: "Logs",
			icon: "paste",
            callback: function(key, opt){
                
            }
		}
    }
});