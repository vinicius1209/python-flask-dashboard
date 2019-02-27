$("#mySearch").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#myNcs tr").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

//Busca pelo click no tr da table, o id da tarefa, ou seja, coluna 0
$("#myNcs tr").on("click", function () {
    var task = $(this).find("td").eq(0).text();
    var modal = "#modalNc" + task;
    $(modal).modal();
});

//Tooltip para cada linha da tabela
$('[data-toggle="tooltip"]').tooltip();

//Obrigado Leonardo
$('.modal').on('shown.bs.modal', function () {
    $(this).find("#id").trigger('focus')
})
