$(document).ready(function() {

    //Gatilho de quando uma tecla for apertada na searchBar pesquisar um registro
    $("#mySearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myEmails tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    //Busca pelo click no tr da table, o id da tarefa, ou seja, coluna 0
    $("#myEmails tr").on("click", function() {
        var task = $(this).find("td").eq(0).text();
        var modal = "#modalEmail" + task;
        $(modal).modal();
    });
});