/************************ DOCUMENT *************************************/
//Barra de pesquisa para pesquisar os componentes na table
$(document).ready(function(){

    $("#mySearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
       $("#myNcs tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    //Busca pelo click no tr da table, o id da tarefa, ou seja, coluna 0
    $("#myNcs tr").on("click", function() {
        var task = $(this).find("td").eq(0).text();
        var modal = "#modalNc" + task;
        $(modal).modal();
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
                //Ao clicar no botão consigo pegar o elemento ID, procurar pela coluna 0 para saber qual tarefa
                //eu vou colocar na requisição, exemplo /forum/27554
                var elem_id = opt.$trigger.attr("id");
                var task_id = $('#' + elem_id).find("td").eq(0).text();
                var win = window.open('/forum/' + task_id, '_blank');
                win.focus();
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